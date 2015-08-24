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
""" A generic helper to manage simple Openstack access credentials"""
from __future__ import unicode_literals
import os
import sys

from keystoneclient.v2_0 import client as ksclient
from oslo_config import cfg

opts = [
    cfg.StrOpt('username', help="Keystone username"),
    cfg.StrOpt('password', help="Keystone password"),
    cfg.StrOpt('auth_url', help="Keystone Auth Url"),
    cfg.StrOpt('tag', help="tag for the generated Image"),
]
CONF = cfg.CONF
CONF.register_cli_opts(opts)
CONF(sys.argv[1:])
USERNAME = os.environ.get('OS_USERNAME', CONF.username)
PASSWORD = os.environ.get('OS_PASSWORD', CONF.password)
AUTH_URL = os.environ.get('AUTH_URL', CONF.auth_url)


def get_credentials():
    creds = {
        'username': USERNAME,
        'password': PASSWORD,
        'auth_url': AUTH_URL,
        'tenant_name': USERNAME,
    }
    return creds


def get_glance_connection():
    creds = get_credentials()
    kc = ksclient.Client(**creds)
    kc.authenticate()
    gdata = {
        'endpoint': kc.service_catalog.url_for(
            service_type='image',
            endpoint_type='publicURL'
        ),
        'token': kc.auth_ref['token']['id']
    }
    return gdata
