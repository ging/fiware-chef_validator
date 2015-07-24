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
from oslo_log import log as logging

from chef_validator.common import wsgi
import chef_validator.common.context

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class ContextMiddleware(wsgi.Middleware):

    @staticmethod
    def process_request(req):
        """Convert authentication information into a request context

        Generate a murano.context.RequestContext object from the available
        authentication headers and store on the 'context' attribute
        of the req object.

        :param req: wsgi request object that will be given the context object
        """

        roles = [r.strip() for r in req.headers.get('X-Roles').split(',')]
        kwargs = {
            'user': req.headers.get('X-User-Id'),
            'auth_token': req.headers.get('X-Auth-Token'),
        }
        req.context = chef_validator.common.context.RequestContext(**kwargs)

    @classmethod
    def factory(cls, global_conf, **local_conf):
        def filter(app):
            return cls(app)
        return filter