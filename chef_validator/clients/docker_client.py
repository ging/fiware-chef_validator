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


class DockerClient:

    def __init__(self, url=CONF.clients_docker.url):
        self._url = url
        self.container = None
        try:
            self.dc = DC(base_url=self._url)
        except Exception as e:
            print e

    def test_recipe(self, recipe, image=CONF.clients_docker.image):
        LOG.debug("Sending recipe to docker server in %s" % self._url)
        b_success = True
        msg = {}
        self.run_container(image)
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
        self.remove_container()
        return msg

    def run_deploy(self, recipe):
        """ Run recipe deployment
        :param recipe: recipe to deploy
        :return msg: dictionary with results and state
        """
        try:
            # inject custom solo.json file
            json_cont = '{"run_list": [ "recipe[%s]"],}' % recipe
            cmd_inject = 'echo %s >/etc/chef/solo.json' % json_cont
            self.execute_command(cmd_inject)
            # launch execution
            cmd_launch = "chef-solo –c /etc/chef/solo.rb -j /etc/chef/solo.json"
            resp_launch = self.execute_command(cmd_launch)
            msg = {
                'success': True,
                'response': resp_launch
            }
            if resp_launch is None or "FATAL" in resp_launch:
                msg['success'] = False
        except Exception as e:
            self.remove_container(self.container)
            LOG.error(_LW("Recipe deployment exception %s" % e))
            raise RecipeDeploymentException(recipe=recipe)
        return msg

    def run_test(self, recipe):
        """ Test cookbook syntax
        :param recipe: recipe to test
        :return msg: dictionary with results and state
        """
        try:
            cmd_test = "knife cookbook test %s" % recipe
            resp_test = self.execute_command(cmd_test)
            msg = {
                'success': True,
                'response': resp_test
            }
            for line in resp_test.splitlines():
                if "ERROR" in line:
                    msg['success'] = False
        except Exception as e:
            self.remove_container(self.container)
            LOG.error(_LW("Cookbook syntax exception %s" % e))
            raise CookbookSyntaxException(recipe=recipe)
        return msg

    def run_install(self, recipe):
        try:
            cmd_install = "knife cookbook github install cookbooks/%s" % recipe
            resp_install = self.execute_command(cmd_install)
            msg = {
                'success': True,
                'response': resp_install
            }
            for line in resp_install.splitlines():
                if "ERROR" in line:
                    msg['success'] = False
        except Exception as e:
            self.remove_container(self.container)
            LOG.error(_LW("Chef install exception %s" % e))
            raise CookbookInstallException(recipe=recipe)
        return msg

    def run_container(self, image):
        """Run and start a container based on the given image
        :param image: image to run
        :return:
        """
        self.container = None
        try:
            self.container = self.dc.create_container(image, tty=True, name="%s-validate" % image)
            self.dc.start(container=self.container.get('Id'))
        except Exception as e:
            LOG.error(_LW("Error creating container %s" % e))
            raise DockerContainerException(image=image)

    def remove_container(self, kill=True):
        """destroy container on exit
        :param kill: inhibits removal for testing purposes
        """
        self.dc.stop(self.container)
        if kill:
            self.dc.remove_container(self.container)

    def execute_command(self, command):
        """ Execute a command in the given container
        :param command:  bash command to run
        :return:  execution result
        """
        bash_txt = "/bin/bash -c \'{}\'".format(command)
        print bash_txt
        exec_txt = self.dc.exec_create(container=self.container.get('Id'), cmd=bash_txt)
        return self.dc.exec_start(exec_txt.get('Id'))

if __name__ == '__main__':
    import logging
    LOG = logging.getLogger()
    logging.basicConfig(level=logging.DEBUG)
    d = DockerClient()
    import pprint
    pprint.pprint(d.test_recipe("patata", image="pmverdugo/chef-solo"))
