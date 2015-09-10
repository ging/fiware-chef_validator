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
""" Tests for chef_validator.api.middleware.context """
from __future__ import unicode_literals

import mock
from chef_validator.api.middleware.context import ContextMiddleware
from chef_validator.api.middleware.context import RequestContext

from chef_validator.tests.base import ValidatorTestCase


class ContextMiddlewareTestCase(ValidatorTestCase):
    """ Tests for class ContextMiddleware """

    def setUp(self):
        """ Create a ContextMiddleware instance """
        super(ContextMiddlewareTestCase, self).setUp()
        self.item = ContextMiddleware()


    def test_make_context(self):
        """ Tests for method make_context """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.make_context(input)
        self.assertEqual(expected, observed)

    def test_process_request(self):
        """ Tests for method process_request """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.process_request(input)
        self.assertEqual(expected, observed)

    def tearDown(self):
        """ Cleanup the ContextMiddleware instance """
        super(ContextMiddlewareTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class RequestContextTestCase(ValidatorTestCase):
    """ Tests for class RequestContext """

    def setUp(self):
        """ Create a RequestContext instance """
        super(RequestContextTestCase, self).setUp()
        self.item = RequestContext()


    def test_to_dict(self):
        """ Tests for method to_dict """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.to_dict(input)
        self.assertEqual(expected, observed)

    def test_from_dict(self):
        """ Tests for method from_dict """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.from_dict(input)
        self.assertEqual(expected, observed)

    def test_auth_plugin(self):
        """ Tests for method auth_plugin """
        self.item.external = mock.MagicMock()
        input = "MyInput"
        expected = "OK"
        self.item.external.return_value = "OK"
        observed = self.item.auth_plugin(input)
        self.assertEqual(expected, observed)

    def tearDown(self):
        """ Cleanup the RequestContext instance """
        super(RequestContextTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
