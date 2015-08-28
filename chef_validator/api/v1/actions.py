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
from webob import exc

from chef_validator.clients.docker_client import DockerClient
from chef_validator.common import wsgi
from chef_validator.common import exception
from chef_validator.common.i18n import _LI, _
from chef_validator.clients.nova import NovaClient
import chef_validator.common.utils

LOG = logging.getLogger(__name__)


class ValidateController(object):
    """
    Validate Controller Object
    Implements Application logic
    """

    @staticmethod
    def validate(request, body):
        body = body or {}
        if len(body) < 1:
            raise exc.HTTPBadRequest(_("No action specified"))
        try:
            recipe = body['recipe']
            image = body['image']
        except KeyError:
            raise exc.HTTPBadRequest(_("Insufficient payload"))

        LOG.info(_LI('Processing Request'))
        n = NovaClient(request.context)

        # find the image id
        image = n.get_image_by_name(image)
        if not image:
            raise exception.ImageNotFound

        machine = "%s-validate" % body['image']

        # if the machine already exists, destroy it
        if n.get_machine(machine):
            LOG.info(_LI("Server %s already exists, deleting" % machine))
            n.delete_machine(machine)

        # deploy machine
        n.deploy_machine(machine, image=image['name'])
        ip = n.get_ip()

        # send knife command
        # c = ChefClient(ip)
        d = DockerClient()
        res = d.recipe_deployment_test(recipe)
        return res


def create_resource():
    """
    Actions action factory method.
    """
    deserializer = chef_validator.common.utils.JSONDeserializer()
    serializer = chef_validator.common.utils.JSONSerializer()
    return wsgi.Resource(ValidateController(), deserializer, serializer)
