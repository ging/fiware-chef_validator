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

import routes

from chef_validator.api.v1 import actions
from chef_validator.common import wsgi


class API(wsgi.Router):
    """
    WSGI router for chef_validator v1 ReST API requests.
    """

    def __init__(self, conf, **local_conf):
        self.conf = conf
        mapper = routes.Mapper()
        actions_resource = actions.create_resource()
        mapper.connect('/validate', controller=actions_resource,
                       action='validate', conditions={'method': ['POST']})
        super(API, self).__init__(mapper)
