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
"""Chef client tests"""
from __future__ import unicode_literals
import mock
from oslo_config import cfg
from chef_validator.clients.chef_client_ssh import ChefClientSSH
from chef_validator.common.exception import SshConnectException
import chef_validator.tests.unit.base as tb

CONF = cfg.CONF
CONF.import_group('clients_chef', 'chef_validator.clients.chef_client_ssh')


class ChefClientTestCase(tb.ValidatorTestCase):
    """Chef Client unit tests"""

    def setUp(self):
        """Create a chef client"""
        super(ChefClientTestCase, self).setUp()
        self.client = ChefClientSSH("1.1.1.1")
        CONF.set_override('cmd_test', "cmdtest {}", group='clients_chef')
        CONF.set_override('cmd_install', "cmdinstall {}", group='clients_chef')
        CONF.set_override('cmd_inject', "cmdinject {}", group='clients_chef')
        CONF.set_override('cmd_launch', "cmdlaunch {}", group='clients_chef')
        CONF.set_override('cmd_config', "cmdconfig {}", group='clients_chef')

    def test_connect_session(self):
        """Test client creation"""
        self.client.ssh = mock.MagicMock()
        self.client.ssh.connect.return_value = "OK"
        expected = None
        observed = self.client.connect_session()
        self.assertEqual(expected, observed)


    def test_disconnect_session(self):
        """Test stopping and removing a container"""
        self.client.ssh = mock.MagicMock()
        self.client.disconnect_session()
        self.client.ssh.disconnect.assert_called_once_with()

    def test_run_deploy(self):
        self.client.execute_command = self.m.CreateMockAnything()
        self.client.ssh = mock.MagicMock()
        self.client.container = "1234"
        self.client.execute_command(
            'cmdinject cmdconfig fakecookbook'
        ).AndReturn("Alls good")
        self.client.execute_command('cmdlaunch {}').AndReturn("Alls good")
        self.m.ReplayAll()
        obs = self.client.run_deploy("fakecookbook")
        expected = "{'response': u'Alls good', 'success': True}"
        self.assertEqual(expected, str(obs))
        self.m.VerifyAll()

    def test_run_install(self):
        self.client.execute_command = self.m.CreateMockAnything()
        self.client.container = "1234"
        self.client.execute_command(
            'cmdinstall fakecookbook'
        ).AndReturn("Alls good")
        self.m.ReplayAll()
        obs = self.client.run_install("fakecookbook")
        expected = "{'response': u'Alls good', 'success': True}"
        self.assertEqual(expected, str(obs))
        self.m.VerifyAll()

    def test_run_test(self):
        self.client.execute_command = self.m.CreateMockAnything()
        self.client.container = "1234"
        self.client.execute_command(
            'cmdtest fakecookbook'
        ).AndReturn("Alls good")
        self.m.ReplayAll()
        obs = self.client.run_test("fakecookbook")
        expected = "{'response': u'Alls good', 'success': True}"
        self.assertEqual(expected, str(obs))
        self.m.VerifyAll()

    def test_execute_command(self):
        """Test a command execution in container"""
        self.client.ssh = self.m.CreateMockAnything()
        stdin = mock.MagicMock()
        self.client.ssh.exec_command(
            u'mycommand'
        ).AndReturn((stdin, "OK", None))
        self.m.ReplayAll()
        obs = self.client.execute_command("mycommand")
        self.assertEqual("OK", obs)
        self.m.VerifyAll()

    def tearDown(self):
        """Cleanup environment"""
        super(ChefClientTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
