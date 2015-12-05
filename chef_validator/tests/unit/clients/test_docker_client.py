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
"""Docker client tests"""
from __future__ import unicode_literals
import mock
import docker
from docker.errors import DockerException
from oslo_config import cfg
from chef_validator.common.exception import DockerContainerException
import chef_validator.tests.unit.base as tb
from chef_validator.clients.docker_client import DockerClient

CONF = cfg.CONF
CONF.import_group('clients_chef', 'chef_validator.clients.chef_client_ssh')


class DockerClientTestCase(tb.ValidatorTestCase):
    """Docker Client unit tests"""

    def setUp(self):
        """Create a docker client"""
        super(DockerClientTestCase, self).setUp()
        self.client = DockerClient()
        CONF.set_override(
            'cmd_test',
            "knife cookbook test {cookbook_name}",
            group='clients_chef')
        CONF.set_override(
            'cmd_install',
            " knife cookbook site install {cookbook_name}",
            group='clients_chef')
        CONF.set_override('cmd_inject', "cmdinject {}", group='clients_chef')
        CONF.set_override('cmd_launch', "cmdlaunch {}", group='clients_chef')

    def test_create_client(self):
        """Test client creation"""
        self.assertRaises(DockerException, DockerClient, 'fakeurl')
        self.assertIsInstance(self.client.dc, docker.client.Client)

    def test_run_container(self):
        """Test container deployment"""
        self.client.dc = mock.MagicMock()
        self.client.run_container('validimage')
        self.client.dc.create_container.assert_called_once_with(
            'validimage',
            name=u'validimage-validate',
            tty=True)
        self.client.dc.start.assert_called_once_with(
            container=self.client.container
        )

    def test_stop_container(self):
        """Test stopping and removing a container"""
        self.client.dc = self.m.CreateMockAnything()
        self.client.dc.stop(self.client.container)
        self.client.dc.remove_container(self.client.container)
        self.m.ReplayAll()
        self.client.remove_container()
        self.m.VerifyAll()

    def test_run_deploy(self):
        self.client.remove_container = mock.MagicMock()
        self.client.execute_command = mock.MagicMock()
        self.client.execute_command.return_value = "Alls good"
        obs = self.client.run_deploy("mycookbook", "myrecipe")
        expected = "{'response': u'Alls good', 'success': True}"
        self.assertEqual(expected, str(obs))

    def test_run_install(self):
        self.client.container = "1234"
        self.client.remove_container = mock.MagicMock()
        self.client.execute_command = mock.MagicMock()
        self.client.execute_command.return_value = "Alls good"
        cookbook = "testing"
        obs = self.client.run_install(cookbook)
        expected = "{'response': u'Alls good', 'success': True}"
        self.assertEqual(expected, str(obs))

    def test_run_test(self):
        self.client.remove_container = mock.MagicMock()
        self.client.execute_command = mock.MagicMock()
        self.client.execute_command.return_value = "Alls good"
        test_input = "testing"
        cookbook = test_input
        obs = self.client.run_test(cookbook)
        expected = "{'response': u'Alls good', 'success': True}"
        self.assertEqual(expected, str(obs))
        self.m.VerifyAll()

    def test_execute_command(self):
        """Test a command execution in container"""
        self.client.dc = self.m.CreateMockAnything()
        self.client.container = "1234"
        self.client.dc.exec_create(
            cmd='/bin/bash -c "mycommand"',
            container=u'1234'
        ).AndReturn("validcmd")
        self.client.dc.exec_start("validcmd").AndReturn("OK")
        self.m.ReplayAll()
        obs = self.client.execute_command("mycommand")
        self.assertEqual("OK", obs)
        self.m.VerifyAll()

    def tearDown(self):
        """Cleanup environment"""
        super(DockerClientTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
