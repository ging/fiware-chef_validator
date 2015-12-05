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
"""Tests for chef_validator.engine.validate """
from mock import mock
import docker.errors

from chef_validator.engine.validate import ValidateEngine
from chef_validator.tests.unit.base import ValidatorTestCase


class ValidateEngineTestCase(ValidatorTestCase):
    """Tests for class ValidateEngine """

    def setUp(self):
        """Create a ValidateEngine instance """
        super(ValidateEngineTestCase, self).setUp()
        self.validate = ValidateEngine()

    def test_validate_cookbook(self):
        """Tests for method validate_cookbook """
        self.validate.d.cookbook_deployment_test = mock.MagicMock(
            return_value="OK")
        test_input = "MyInput"
        cookbook = recipe = image = request = test_input
        expected = "OK"
        observed = self.validate.validate_cookbook(
                              cookbook,
                              recipe,
                              image,
                              request)
        self.assertEqual(observed, expected)


    def tearDown(self):
        """Cleanup the ValidateEngine instance """
        super(ValidateEngineTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
