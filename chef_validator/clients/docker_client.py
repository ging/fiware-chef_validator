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
from docker.errors import DockerException
from oslo_log import log as logging
from oslo_config import cfg
from docker import Client as DC

from chef_validator.common.exception import CookbookSyntaxException, \
    RecipeDeploymentException, \
    CookbookInstallException, \
    DockerContainerException
from chef_validator.common.i18n import _LW, _LE

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('url', default='unix://var/run/docker.sock'),
    cfg.StrOpt('image'),
]
CONF = cfg.CONF
CONF.register_opts(opts, group="clients_docker")


class DockerClient(object):
    """
    Wrapper for Docker client
    """

    def __init__(self, url=CONF.clients_docker.url):
        self._url = url
        self.container = None
        try:
            self.dc = DC(base_url=self._url)
        except DockerException as e:
            LOG.error(_LE("Docker client error: %s") % e)
            raise e

    def test_recipe(self, recipe, image=CONF.clients_docker.image):
        """
        Try to process a recipe and return results
        :param recipe: recipe to deploy
        :param image: image to deploy to
        :return: dictionary with results
        """
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
            self.remove_container(self.container)
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
            self.remove_container(self.container)
            LOG.error(_LW("Chef install exception: %s" % e))
            raise CookbookInstallException(recipe=recipe)
        return msg

    def run_container(self, image):
        """Run and start a container based on the given image
        :param image: image to run
        :return:
        """
        contname = "%s-validate" % image
        try:
            self.container = self.dc.create_container(
                image,
                tty=True,
                name=contname
            )
            self.dc.start(container=self.container.get('Id'))
        except AttributeError as e:
            LOG.error(_LW("Error creating container: %s" % e))
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
        exec_txt = self.dc.exec_create(
            container=self.container.get('Id'),
            cmd=bash_txt
        )
        return self.dc.exec_start(exec_txt.get('Id'))


if __name__ == '__main__':
    import logging

    LOG = logging.getLogger()
    logging.basicConfig(level=logging.DEBUG)
    d = DockerClient("fakeurl")
    import pprint

    pprint.pprint(d.test_recipe("patata", image="pmverdugo/chef-solo"))
