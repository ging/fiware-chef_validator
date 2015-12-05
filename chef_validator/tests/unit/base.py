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
import mox

from oslo_config import cfg
from chef_validator.common import log
import testtools
import fixtures

CONF = cfg.CONF
log.setup(CONF, 'chef_validator')


class ValidatorTestCase(testtools.TestCase):
    """Default test environment setter"""

    def setUp(self):
        """setup logger fixture"""
        super(ValidatorTestCase, self).setUp()
        # self.useFixture(fixtures.FakeLogger())
        self.useFixture(fixtures.WarningsCapture())
        self.m = mox.Mox()
        self.addCleanup(self.m.UnsetStubs)

    def override_config(self, name, override, group=None):
        """
        overload config settings
        :param name:  config element name
        :param override: new config value
        :param group: config element group
        :return:
        """
        CONF.set_override(name, override, group)
        self.addCleanup(CONF.clear_override, name, group)
