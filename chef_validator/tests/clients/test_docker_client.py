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
""" Docker client tests"""
from __future__ import unicode_literals
import docker
from docker.errors import DockerException
from oslo_utils.tests.test_excutils import mox
from testtools import ExpectedException
import testtools
from chef_validator.common.exception import DockerContainerException
import chef_validator.tests.base as tb
from chef_validator.clients.docker_client import DockerClient


class DockerClientTestCase(tb.ValidatorTestCase):
    """Docker Client unit tests"""

    def setUp(self):
        """ Create a docker client"""
        super(DockerClientTestCase, self).setUp()
        self.client = DockerClient()
        self.mox = mox.Mox()

    def test_create_client(self):
        """ Test client creation"""
        self.assertRaises(DockerException, DockerClient, 'fakeurl')
        self.assertIsInstance(self.client.dc, docker.client.Client)

    def test_run_container(self):
        """ Test container deployment"""
        self.assertRaises(DockerContainerException, self.client.run_container, "fakeimage")
        # self.client.dc = self.mox.CreateMockAnything()
        # self.client.dc.create_container('validimage', name='validimage-validate', tty=True)
        # self.client.container = self.mox.CreateMockAnything()
        # self.client.dc.start(container=self.client.container.get('Id'))
        # self.mox.ReplayAll()
        # self.client.run_container("validimage")
        # self.mox.VerifyAll()

    def test_stop_container(self):
        """ Test stopping and removing a container"""
        self.client.dc = self.mox.CreateMockAnything()
        self.client.dc.stop(self.client.container)
        self.client.dc.remove_container(self.client.container)
        self.mox.ReplayAll()
        self.client.remove_container()
        self.mox.VerifyAll()

    def tearDown(self):
        """ Cleanup environment"""
        super(DockerClientTestCase, self).tearDown()
        self.mox.UnsetStubs()
        self.mox.ResetAll()
