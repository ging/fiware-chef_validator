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
from keystoneclient.v2_0 import client as ksclient


class KeystoneClient(object):
    def __init__(self, context):
        settings = self._get_keystone_settings()
        kwargs = {
            'token': context['auth_token'],
            'endpoint': settings['endpoint'],
            'auth_url': settings['auth_url'],
            'project_name': context['project']['name']
        }
        self.kc = ksclient.Client(**kwargs)
        self.kc.authenticate()

    @staticmethod
    def _get_keystone_settings():
        importutils.import_module('keystonemiddleware.auth_token')
        return {
            'endpoint': cfg.CONF.keystone_authtoken.identity_uri,
            'auth_url': cfg.CONF.keystone_authtoken.auth_uri,
            'username': cfg.CONF.keystone_authtoken.admin_user,
            'password': cfg.CONF.keystone_authtoken.admin_password,
            'project_name': cfg.CONF.keystone_authtoken.admin_tenant_name}
