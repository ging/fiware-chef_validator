#!/usr/bin/env python
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
"""Tests for chef_validator.clients.glance_client """
from __future__ import unicode_literals
import mock
from oslo_config import cfg
from chef_validator.clients.glance_client import AmbiguousNameException
from chef_validator.clients.glance_client import GlanceClient
from chef_validator.tests.unit.base import ValidatorTestCase

CONF = cfg.CONF
CONF.import_group('clients_glance', 'chef_validator.clients.glance_client')


class AmbiguousNameExceptionTestCase(ValidatorTestCase):
    """Tests for class AmbiguousNameException """

    def setUp(self):
        """Create a AmbiguousNameException instance """
        super(AmbiguousNameExceptionTestCase, self).setUp()
        self.item = AmbiguousNameException()

    def tearDown(self):
        """Cleanup the AmbiguousNameException instance """
        super(AmbiguousNameExceptionTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class GlanceClientTestCase(ValidatorTestCase):
    """Tests for class GlanceClient """

    def setUp(self):
        """Create a GlanceClient instance """
        super(GlanceClientTestCase, self).setUp()
        keystone_client = mock.MagicMock()
        CONF.set_override('endpoint', "1234", group='clients_glance')
        self.client = GlanceClient(keystone_client)
        self.client._client = mock.MagicMock()

    def test_list(self):
        """Tests for method list """
        self.client._client.images.list = mock.MagicMock()
        self.client._client.images.list.return_value = (mock.MagicMock()
                                                        for n in range(2))
        observed = tuple(self.client.list())
        expected = ("1", "2")
        self.assertEqual(len(expected), len(observed))

    def test_get_by_name(self):
        """Tests for method get_by_name """
        input = "MyInput"
        expected = None
        observed = self.client.get_by_name(input)
        self.assertEqual(expected, observed)

    def test_getById(self):
        """Tests for method getById """
        self.client._client.images.get.return_value = mock.MagicMock()
        expected = {"id": "myid", "name": "myname"}
        observed = self.client.getById("1234")
        self.assertEqual(len(expected.items()), len(observed.items()))

    def test_create_glance_client(self):
        """Tests for method create_glance_client """
        keystone_client = mock.MagicMock()
        keystone_client.auth_token = "1234"
        keystone_client.service_catalog = mock.MagicMock()
        self.client._client = mock.MagicMock()
        observed = self.client.create_glance_client(keystone_client)
        expected = None
        self.assertEqual(expected, observed)

    def tearDown(self):
        """Cleanup the GlanceClient instance """
        super(GlanceClientTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
