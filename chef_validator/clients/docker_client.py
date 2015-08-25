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


from oslo_log import log as logging
from oslo_config import cfg
from docker import Client as DC
from chef_validator.common.exception import CookbookSyntaxException, RecipeDeploymentException, \
    CookbookInstallException, DockerContainerException

from chef_validator.common.i18n import _, _LW

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('url', default='unix://var/run/docker.sock'),
    cfg.StrOpt('image'),
]
CONF = cfg.CONF
CONF.register_opts(opts, group="clients_docker")


class DockerClient(object):

    def __init__(self, url=CONF.clients_docker.url):
        self._url = url
        try:
            self.dc = DC(base_url=self._url)
        except Exception as e:
            print e

    def test_recipe(self, recipe, image=CONF.clients_docker.image):
        LOG.debug("Sending recipe to docker server in %s" % self._url)

        # run container
        # try:
        container = self.dc.create_container(image)
        self.dc.start(container=container.get('Id'))
        # except Exception as e:
        #     LOG.error(_LW("Error creating container %s" % e))
        #     raise DockerContainerException(image=image)

        # install cookbook
        try:
            cmd_install = "knife cookbook github install cookbooks/%s" % recipe
            bash_install = "/bin/bash -c \'{}\'".format(cmd_install)
            exec_install = self.dc.exec_create(container=image, cmd=bash_install)
            resp_install = self.dc.exec_start(exec_install.get('Id'))
            print resp_install
        except Exception as e:
            LOG.error(_LW("Chef install exception %s" % e))
            raise CookbookInstallException(recipe=recipe)

        # test cookbook syntax
        try:
            cmd_test = "knife cookbook test %s" % recipe
            bash_test = "/bin/bash -c \'{}\'".format(cmd_test)
            exec_test = self.dc.exec_create(container=image, cmd=bash_test)
            resp_test = self.dc.exec_start(exec_test.get('Id'))
            print resp_test
        except Exception as e:
            LOG.error(_LW("Cookbook syntax exception %s" % e))
            raise CookbookSyntaxException(recipe=recipe)

        # launch recipe deployment
        try:
            cmd_launch = "Chef-solo –c /etc/chef/solo.rb -j /etc/chef/solo.json"
            bash_launch = "/bin/bash -c \'{}\'".format(cmd_launch)
            exec_launch = self.dc.exec_create(container=image, cmd=bash_launch)
            resp_launch = self.dc.exec_start(exec_launch.get('Id'))
            print resp_launch
        except Exception as e:
            LOG.error(_LW("Recipe deployment exception %s" % e))
            raise RecipeDeploymentException(recipe=recipe)

        # check execution output
        if resp_launch is None or "FATAL" in resp_launch:
            # better to provide server error messages (500) to the client
            msg = "Error deploying recipe %s" % recipe
            LOG.error(_LW(msg))
        else:
            msg = _("Recipe %s successfully deployed" % recipe)
        return msg

if __name__ == '__main__':
    d = DockerClient()
    d.test_recipe("git", image="pmverdugo/chef-solo")
