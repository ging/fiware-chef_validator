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
from chef_validator.common.i18n import _LI
from chef_validator.engine.clients.glance import GlanceClient
from chef_validator.engine.clients.keystone import KeystoneClient

LOG = logging.getLogger(__name__)


class ValidateController(object):
    """
    Validate Controller Object
    Implements Application logic
    """
    def validate(self, request, body):
        LOG.info(_LI('Processing Request'))
        c = request.context
        ks = KeystoneClient(c.auth_token)
        g = GlanceClient(ks.kc)
        g.get_by_name(body['recipe']['machine'])

        return {"resp": "OK"}


def create_resource():
    """
    Actions action factory method.
    """
    deserializer = wsgi.JSONDeserializer()
    serializer = wsgi.JSONSerializer()
    return wsgi.Resource(ValidateController(), deserializer, serializer)
