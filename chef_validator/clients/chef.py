# -*- coding: utf-8 -*-
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import paramiko
from oslo_log import log as logging
from oslo_config import cfg
from chef_validator.common.exception import SshConnectException, CookbookSyntaxException, RecipeDeploymentException, \
    CookbookInstallException

from chef_validator.common.i18n import _, _LW

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('username'),
    cfg.StrOpt('password'),
]
CONF = cfg.CONF
CONF.register_opts(opts, group="clients_chef")


class ChefClient(object):

    def __init__(self, ip):
        self._ip = ip
        self._username = CONF.clients_chef.username
        self._password = CONF.clients_chef.password

    def send_recipe(self, recipe):
        msg = _("Unknown")
        LOG.debug("Sending recipe to %s" % self._ip)

        # connecto to machine
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self._ip,
                        username=CONF.username,
                        password=CONF.password
                        )
        except Exception as e:
            LOG.error(_LW("SSH connect exception %s" % e))
            raise SshConnectException(host=self._ip)

        # install cookbook
        try:
            stdin, stdout, stderr = ssh.exec_command(
                "knife cookbook github install cookbooks/%s" % recipe
            )
            stdin.flush()
        except Exception as e:
            LOG.error(_LW("SSH command send exception %s" % e))
            raise CookbookInstallException(recipe=recipe)

        # test cookbook syntax
        try:
            stdin, stdout, stderr = ssh.exec_command(
                "knife cookbook test %s" % recipe
            )
            stdin.flush()
        except Exception as e:
            LOG.error(_LW("Cookbook syntax exception %s" % e))
            raise CookbookSyntaxException(recipe=recipe)

        # launch recipe deployment
        try:
            stdin, stdout, stderr = ssh.exec_command(
                "Chef-solo –c /etc/chef/solo.rb -j /etc/chef/solo.json"
            )
            stdin.flush()
        except Exception as e:
            LOG.error(_LW("Recipe deployment exception %s" % e))
            raise RecipeDeploymentException(recipe=recipe)

        # check execution output
        if stdout is None or "FATAL" in stdout:
            # better to provide server error messages (500) to the client
            msg = "Error deploying recipe %s" % recipe
            LOG.error(_LW(msg))
        else:
            msg = _("Recipe %s successfully deployed" % recipe)
        return msg
