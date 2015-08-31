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
from eventlet import websocket

from oslo_log import log as logging
from oslo_config import cfg

from chef_validator.common.exception import SshConnectException, CookbookSyntaxException, RecipeDeploymentException, \
    CookbookInstallException, SerialConnectException
from chef_validator.common.i18n import _LW

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('cmd_install'),
    cfg.StrOpt('cmd_config'),
    cfg.StrOpt('cmd_inject'),
    cfg.StrOpt('cmd_test'),
    cfg.StrOpt('cmd_launch')
]
CONF = cfg.CONF
CONF.register_opts(opts, group="clients_chef")


class ChefClientSerial(object):
    """ Chef client wrapper"""

    def __init__(self, sercon):
        """
        set internal parameters
        :param sercon: serial connection url as given by novaclient
        """
        self._sercon = sercon
        self.serial = None

    def recipe_deploy_test(self, recipe):
        """ Try to deploy the given recipe through an serial connection
        :param recipe: recipe to deploy
        :return: dict message with results
        """
        LOG.debug("Sending recipe to %s" % self._sercon)
        b_success = True
        msg = {}
        self.connect_session()
        msg['install'] = self.run_install(recipe)
        b_success &= msg['install']['success']
        msg['test'] = self.run_test(recipe)
        b_success &= msg['test']['success']
        msg['deploy'] = self.run_deploy(recipe)
        b_success &= msg['deploy']['success']

        # check execution output
        if b_success:
            msg['result'] = {
                'success': True,
                'result': "Recipe %s successfully deployed\n" % recipe
            }
        else:
            msg['result'] = {
                'success': False,
                'result': "Error deploying recipe {}\n".format(recipe)
            }
            LOG.error(_LW(msg))
        self.disconnect_session()
        return msg

    def run_deploy(self, recipe):
        """ Run recipe deployment
        :param recipe: recipe to deploy
        :return msg: dictionary with results and state
        """
        try:
            # inject custom solo.json file
            json_cont = CONF.clients_chef.cmd_config % recipe
            cmd_inject = CONF.clients_chef.cmd_inject.format(json_cont)
            self.execute_command(cmd_inject)
            # launch execution
            cmd_launch = CONF.clients_chef.cmd_launch
            resp_launch = self.execute_command(cmd_launch)
            msg = {
                'success': True,
                'response': resp_launch
            }
            if resp_launch is None or "FATAL" in resp_launch:
                msg['success'] = False
        except Exception as e:
            self.disconnect_session()
            LOG.error(_LW("Recipe deployment exception %s" % e))
            raise RecipeDeploymentException(recipe=recipe)
        return msg

    def run_test(self, recipe):
        """ Test cookbook syntax
        :param recipe: recipe to test
        :return msg: dictionary with results and state
        """
        try:
            cmd_test = CONF.clients_chef.cmd_test.format(recipe)
            resp_test = self.execute_command(cmd_test)
            msg = {
                'success': True,
                'response': resp_test
            }
            for line in resp_test.splitlines():
                if "ERROR" in line:
                    msg['success'] = False
        except Exception as e:
            self.disconnect_session()
            LOG.error(_LW("Cookbook syntax exception %s" % e))
            raise CookbookSyntaxException(recipe=recipe)
        return msg

    def run_install(self, recipe):
        """Run download and install command
        :param recipe: recipe to process
        :return msg: operation result
        """
        try:
            cmd_install = CONF.clients_chef.cmd_install.format(recipe)
            resp_install = self.execute_command(cmd_install)
            msg = {
                'success': True,
                'response': resp_install
            }
            for line in resp_install.splitlines():
                if "ERROR" in line:
                    msg['success'] = False
        except Exception as e:
            self.disconnect_session()
            LOG.error(_LW("Chef install exception %s" % e))
            raise CookbookInstallException(recipe=recipe)
        return msg

    def connect_session(self):
        """
        Connect to a session with the internal parameters
        :return:
        """
        try:
            self.serial = websocket.create_connection(
                self._sercon,
                subprotocols=['binary', 'base64'])()
        except Exception as e:
            LOG.error(_LW("Serial connect exception %s" % e))
            raise SerialConnectException(host=self._sercon)

    def disconnect_session(self):
        """close session on exit
        """
        self.serial.disconnect()

    def execute_command(self, command):
        """ Execute a command in the given container
        :param command:  bash command to run
        :return:  execution result
        """
        stdout = self.serial.snd(command).rcv()
        return stdout
