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
"""Tests for chef_validator.common.utils """
from __future__ import unicode_literals
import mock
from chef_validator.common.utils import JSONDeserializer
from chef_validator.common.utils import JSONSerializer
from chef_validator.tests.unit.base import ValidatorTestCase


class JSONDeserializerTestCase(ValidatorTestCase):
    """Tests for class JSONDeserializer """

    def setUp(self):
        """Create a JSONDeserializer instance """
        super(JSONDeserializerTestCase, self).setUp()
        self.item = JSONDeserializer()

    def test_dispatch(self):
        """Tests for method dispatch """
        input = mock.MagicMock()
        input.body = '{"MyInput": "mydata"}'
        expected = {u'body': {u'MyInput': u'mydata'}}
        observed = self.item.dispatch(input, action="default")
        self.assertEqual(expected, observed)

    def test_deserialize(self):
        """Tests for method deserialize """
        self.item.external = mock.MagicMock()
        input = mock.MagicMock()
        input.body = '{"MyInput": "mydata"}'
        expected = {u'body': {u'MyInput': u'mydata'}}
        self.item.external.return_value = "OK"
        observed = self.item.deserialize(input)
        self.assertEqual(expected, observed)

    def test_default(self):
        """Tests for method default """
        self.item.external = mock.MagicMock()
        request = mock.MagicMock()
        request.body = '{"MyInput": "mydata"}'
        expected = {u'body': {u'MyInput': u'mydata'}}
        self.item.external.return_value = "OK"
        observed = self.item.default(request)
        self.assertEqual(expected, observed)

    def tearDown(self):
        """Cleanup the JSONDeserializer instance """
        super(JSONDeserializerTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class JSONSerializerTestCase(ValidatorTestCase):
    """Tests for class JSONSerializer """

    def setUp(self):
        """Create a JSONSerializer instance """
        super(JSONSerializerTestCase, self).setUp()
        self.item = JSONSerializer()

    def test_default(self):
        """Tests for method default """
        input = "MyInput"
        response = mock.MagicMock()
        result = input
        expected = "\"" + input + "\""
        self.item.default(response, result)
        observed = response.body
        self.assertEqual(expected, observed)

    def tearDown(self):
        """Cleanup the JSONSerializer instance """
        super(JSONSerializerTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
