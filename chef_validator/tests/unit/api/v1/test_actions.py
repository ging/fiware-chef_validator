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
"""Tests for chef_validator.api.v1.actions """
from mock import mock
from oslo_config import cfg

from chef_validator.api.v1.actions import ValidateController
from chef_validator.tests.unit.base import ValidatorTestCase


CONF = cfg.CONF
CONF.import_group('clients_docker', 'chef_validator.clients.docker_client')


class ActionControllerTestCase(ValidatorTestCase):
    """Tests for class ValidateController """

    def setUp(self):
        """Create a ValidateController instance """
        super(ActionControllerTestCase, self).setUp()
        CONF.set_override('url', "url", group='clients_docker')
        self.action = ValidateController()

    def test_validate(self):
        """Tests for method validate """
        self.action.ve.validate_cookbook = mock.MagicMock(return_value="OK")
        req = "MyInput"
        body = {"cookbook": "fakecb", "image": "fakeimg"}
        expected = "OK"
        observed = self.action.validate(req, body)
        self.assertEqual(expected, observed)


    def tearDown(self):
        """Cleanup the ValidateController instance """
        super(ActionControllerTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
