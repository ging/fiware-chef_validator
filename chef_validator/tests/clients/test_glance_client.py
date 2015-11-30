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
""" Tests for chef_validator.clients.glance_client """
from __future__ import unicode_literals

import mock
from chef_validator.clients.glance_client import AmbiguousNameException
from chef_validator.clients.glance_client import GlanceClient

from chef_validator.tests.base import ValidatorTestCase


class AmbiguousNameExceptionTestCase(ValidatorTestCase):
    """ Tests for class AmbiguousNameException """

    def setUp(self):
        """ Create a AmbiguousNameException instance """
        super(AmbiguousNameExceptionTestCase, self).setUp()
        self.item = AmbiguousNameException()


    def tearDown(self):
        """ Cleanup the AmbiguousNameException instance """
        super(AmbiguousNameExceptionTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class GlanceClientTestCase(ValidatorTestCase):
    """ Tests for class GlanceClient """

    def setUp(self):
        """ Create a GlanceClient instance """
        super(GlanceClientTestCase, self).setUp()
        self.item = GlanceClient(None)


    def test_list(self):
        """ Tests for method list """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.list(input)
        self.assertEqual(expected, observed)

    def test_get_by_name(self):
        """ Tests for method get_by_name """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.get_by_name(input)
        self.assertEqual(expected, observed)

    def test_getById(self):
        """ Tests for method getById """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.getById(input)
        self.assertEqual(expected, observed)

    def test_create_glance_client(self):
        """ Tests for method create_glance_client """
        self.item.keystone_client = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.keystone_client.service_catalog.url_for.return_value = "OK"
        observed = self.item.create_glance_client(input)
        self.assertEqual(expected, observed)

    def tearDown(self):
        """ Cleanup the GlanceClient instance """
        super(GlanceClientTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
