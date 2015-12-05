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

from chef_validator.common import log as logging
from oslo_config import cfg
from chef_validator.common import exception
from chef_validator.common.i18n import _LI
from chef_validator.clients.chef_client_ssh import ChefClientSSH
from chef_validator.clients.docker_client import DockerClient
from chef_validator.clients.nova_client import NovaClient
LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class ValidateEngine(object):
    """Engine for validations"""
    def __init__(self):
        self.d = DockerClient()

    def validate_cookbook(self, cookbook, recipe, image, request):
        """
        Cookbook validation
        :param recipe:
        :param image: name of the image to deploy
        :param cookbook: name of the cookbook to validate
        :param request: request context
        :return:
        """
        # process request based on configuration options
        if hasattr(CONF, 'clients_docker') \
                and hasattr(CONF.clients_docker, 'url') \
                and len(CONF.clients_docker.url) > 1:

            # use direct docker connection, fast and simple
            res = self.d.cookbook_deployment_test(cookbook, recipe, image)
        else:
            # nova client connection
            n = NovaClient(request.context)

            # find the image id
            image = n.get_image_by_name(image)
            if not image:
                raise exception.ImageNotFound

            machine = "%s-validate" % cookbook

            # if the machine already exists, destroy it
            if n.get_machine(machine):
                LOG.info(_LI("Server %s already exists, deleting") % machine)
                n.delete_machine(machine)

            # deploy machine
            n.deploy_machine(machine, image=image['name'])
            ip = n.get_ip()

            # generic ssh connection
            c = ChefClientSSH(ip)
            res = c.cookbook_deploy_test(cookbook)
        return res
