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

import logging

import fixtures
import mock
from oslo_utils import timeutils

from chef_validator.tests.unit import base

TEST_DEFAULT_LOGLEVELS = {'migrate': logging.WARN}


class FakeLogMixin(object):
    """Allow logs to be tested (rather than just disabling
    logging.
    """

    def setup_logging(self):
        # Assign default logs to self.LOG so we can still
        # assert on chef_validator logs.
        self.LOG = self.useFixture(fixtures.FakeLogger(level=logging.DEBUG))
        base_list = set([nlog.split('.')[0]
                         for nlog in logging.Logger.manager.loggerDict])
        for base_name in base_list:
            if base_name in TEST_DEFAULT_LOGLEVELS:
                self.useFixture(fixtures.FakeLogger(
                    level=TEST_DEFAULT_LOGLEVELS[base_name], name=base_name))
            elif base_name != 'chef_validator':
                self.useFixture(fixtures.FakeLogger(name=base_name))


class ApiClient(object):
    pass


class ValidatorApiTestCase(base.ValidatorTestCase, FakeLogMixin):
    # Set this if common.rpc is imported into other scopes so that
    # it can be mocked properly

    def setUp(self):
        super(ValidatorApiTestCase, self).setUp()

        self.setup_logging()

        # Mock the API Classes
        self.mock_api = mock.Mock(ApiClient)
        mock.patch('chef_validator.api', return_value=self.mock_api).start()
        self.addCleanup(mock.patch.stopall)

    def tearDown(self):
        super(ValidatorApiTestCase, self).tearDown()
        timeutils.utcnow.override_time = None

    def _stub_uuid(self, values=[]):
        class FakeUUID(object):
            def __init__(self, v):
                self.hex = v

        mock_uuid4 = mock.patch('uuid.uuid4').start()
        mock_uuid4.side_effect = [FakeUUID(v) for v in values]
        return mock_uuid4
