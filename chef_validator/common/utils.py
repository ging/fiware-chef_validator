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

from __future__ import unicode_literals

import datetime

from oslo_serialization import jsonutils
from chef_validator.common import log as logging

from chef_validator.common import exception
from chef_validator.common.i18n import _

LOG = logging.getLogger(__name__)


class JSONSerializer(object):
    @staticmethod
    def default(response, result):
        response.content_type = 'application/json'

        def sanitizer(obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            return obj

        response.body = jsonutils.dumps(result, default=sanitizer)
        LOG.debug("JSON response : %s" % response)


class JSONDeserializer(object):
    def dispatch(self, *args, **kwargs):
        """Find and call local method.
        :param kwargs:
        :param args:
        """
        action = kwargs.pop('action', 'default')
        action_method = getattr(self, str(action), self.default)
        return action_method(*args, **kwargs)

    def deserialize(self, request, action='default'):
        return self.dispatch(request, action=action)

    @staticmethod
    def default(request):
        try:
            return {'body': jsonutils.loads(request.body)}
        except ValueError:
            raise exception.MalformedRequestBody(
                reason=_("cannot understand JSON"))
