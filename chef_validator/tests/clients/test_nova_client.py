#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Tests for :module:'chef_validator.engine.clients.os.nova'."""

import uuid

import mock
from novaclient import client as nc
from novaclient import exceptions as nova_exceptions
from oslo_config import cfg
import six

from chef_validator.common import exception, context
from chef_validator.clients.nova import NovaClient
from chef_validator.tests.base import ValidatorTestCase

def dummy_context(user='test_username', tenant_id='test_tenant_id',
                  password='password', roles=None, user_id=None,
                  trust_id=None, region_name=None):
    roles = roles or []
    return context.RequestContext.from_dict({
        'tenant_id': tenant_id,
        'tenant': 'test_tenant',
        'username': user,
        'user_id': user_id,
        'password': password,
        'roles': roles,
        'is_admin': False,
        'auth_url': 'http://server.test:5000/v2.0',
        'auth_token': 'abcd1234',
        'trust_id': trust_id,
        'region_name': region_name
    })

class NovaClientTestCase(ValidatorTestCase):
    def setUp(self):
        super(NovaClientTestCase, self).setUp()
        self.client = NovaClient(dummy_context())
        self.client._client = mock.MagicMock()

