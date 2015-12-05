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

import mock
from chef_validator.api.middleware import context
from chef_validator.clients.nova_client import NovaClient
from chef_validator.tests.unit.base import ValidatorTestCase


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
        """Setup Environment"""
        super(NovaClientTestCase, self).setUp()
        NovaClient.create_nova_client = mock.MagicMock()
        self.client = NovaClient(dummy_context())
        self.client._client = mock.MagicMock()

    def test_list(self):
        """Test list function"""
        dummy_image = mock.MagicMock()
        dummy_image.id = "myid"
        dummy_image.name = "myname"
        exp = [{'id': 'myid', 'name': 'myname'}]
        self.client._client.images.list.return_value = [dummy_image]
        self.assertEqual(exp, self.client.list())

    def test_get_image_by_name(self):
        """Test get_image_by_name function"""
        dummy_image = mock.MagicMock()
        dummy_image.id = "myid"
        dummy_image.name = "myname"
        exp = {'id': 'myid', 'name': 'myname'}
        self.client._client.images.list.return_value = [dummy_image]
        self.assertEqual(exp, self.client.get_image_by_name("myname"))

    def test_get_ip(self):
        """Test get_ip function"""
        addresses = {
            'public': [{'version': 4,
                        'addr': '4.5.6.7'},
                       {'version': 6,
                        'addr': '2401:1801:7800:0101:c058:dd33:ff18:04e6'}],
            'private': [{'version': 4,
                         'addr': '10.13.12.13'}]}

        expected = '4.5.6.7'
        self.client._client.servers.ips.return_value = addresses
        observed = self.client.get_ip()
        self.assertEqual(expected, observed)

    def test_get_machine(self):
        """Test get_machine function"""
        self.client._client.servers.find(name="mymachine").return_value = True
        expected = True
        observed = self.client.get_machine("mymachine")
        self.assertEqual(expected, observed)

    def test_deploy_machine(self):
        """Test deploy_machine function"""
        machine = mock.MagicMock()
        self.client._client.servers.create.return_value = machine
        expected = machine
        self.client.deploy_machine("mymachine", "myimage")
        observed = self.client._machine
        self.assertEqual(expected, observed)

    def test_delete_machine(self):
        """Test delete_machine function"""
        machine = mock.MagicMock()
        self.client._client.servers.find.return_value = machine
        self.client.delete_machine("mymachine")
        machine.delete.assert_called_once_with()

    def tearDown(self):
        """Cleanup environment"""
        super(NovaClientTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
