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

from oslo_config import cfg
from oslo_utils import importutils


class RequestContext(object):
    """Stores information about the security context under which the user
    accesses the system, as well as additional request information.
    """

    def __init__(self, auth_token=None, user=None):
        self.auth_token = auth_token
        self.user = user

    @property
    def auth_url(self):
        importutils.import_module('keystonemiddleware.auth_token')
        auth_uri = cfg.CONF.keystone_authtoken.auth_uri
        return auth_uri.replace('v2.0', 'v3')

    def to_dict(self):
        return {
            'user': self.user,
            'auth_token': self.auth_token
        }

    @classmethod
    def from_dict(cls, values):
        return cls(**values)
