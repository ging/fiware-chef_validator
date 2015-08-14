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

from chef_validator.common import wsgi
from chef_validator.common import exception
from chef_validator.common.i18n import _LI
from chef_validator.clients.chef import ChefClient
from chef_validator.clients.glance import GlanceClient
from chef_validator.clients.keystone import KeystoneClient
from chef_validator.clients.nova import NovaClient

LOG = logging.getLogger(__name__)


class ValidateController(object):
    """
    Validate Controller Object
    Implements Application logic
    """
    def validate(self, request, body):
        recipe = body['recipe']
        image = body['image']
        LOG.info(_LI('Processing Request'))
        token = request.environ['keystone.token_info']['token']
        ks = KeystoneClient(token)
        g = GlanceClient(ks.kc)

        # find the image id
        image = g.get_by_name(image)
        if not image:
            raise exception.ImageNotFound

        n = NovaClient(ks.kc)
        machine = "%s-validate" % body['image']
        # if the machine already exists, destroy it
        if n.get_machine(machine):
            LOG.info(_LI("Server %s already exists, deleting" % machine))
            n.delete_machine(machine)
        # deploy machine
        n.deploy_machine(machine, image=image['name'])
        ip = n.get_ip()
        # send knife command
        c = ChefClient(ip)
        res = c.send_recipe(recipe)
        return {"resp": res}


def create_resource():
    """
    Actions action factory method.
    """
    deserializer = wsgi.JSONDeserializer()
    serializer = wsgi.JSONSerializer()
    return wsgi.Resource(ValidateController(), deserializer, serializer)
