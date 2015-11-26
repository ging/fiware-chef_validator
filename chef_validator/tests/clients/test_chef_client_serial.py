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
""" Tests for chef_validator.clients.chef_client_serial """
from __future__ import unicode_literals

import mock
from chef_validator.clients.chef_client_serial import ChefClientSerial

from chef_validator.tests.base import ValidatorTestCase


class ChefClientSerialTestCase(ValidatorTestCase):
    """ Tests for class ChefClientSerial """

    def setUp(self):
        """ Create a ChefClientSerial instance """
        super(ChefClientSerialTestCase, self).setUp()
        self.item = ChefClientSerial()


    def test_cookbook_deploy_test(self):
        """ Tests for method cookbook_deploy_test """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.cookbook_deploy_test(input)
        self.assertEqual(expected, observed)

    def test_run_deploy(self):
        """ Tests for method run_deploy """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.run_deploy(input)
        self.assertEqual(expected, observed)

    def test_run_test(self):
        """ Tests for method run_test """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.run_test(input)
        self.assertEqual(expected, observed)

    def test_run_install(self):
        """ Tests for method run_install """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.run_install(input)
        self.assertEqual(expected, observed)

    def test_connect_session(self):
        """ Tests for method connect_session """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.connect_session(input)
        self.assertEqual(expected, observed)

    def test_disconnect_session(self):
        """ Tests for method disconnect_session """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.disconnect_session(input)
        self.assertEqual(expected, observed)

    def test_execute_command(self):
        """ Tests for method execute_command """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.execute_command(input)
        self.assertEqual(expected, observed)

    def tearDown(self):
        """ Cleanup the ChefClientSerial instance """
        super(ChefClientSerialTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
