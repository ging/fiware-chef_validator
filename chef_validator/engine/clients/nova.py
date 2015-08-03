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

from novaclient import client as nc
from novaclient import exceptions

from oslo_log import log as logging
from oslo_config import cfg

LOG = logging.getLogger(__name__)
opts = [
    cfg.StrOpt('api_version', default='2'),
    cfg.StrOpt('endpoint_type', default='publicURL'),
    cfg.StrOpt('endpoint'),
]
CONF = cfg.CONF
CONF.register_opts(opts, group="clients_nova")


class NovaClient(object):
    def __init__(self, ksc):
        self._client = self.create_nova_client(ksc)
        self._machine = None

    @staticmethod
    def create_nova_client(keystone_client):
        endpoint_type = CONF.clients_nova.endpoint_type
        # nova_endpoint = CONF.clients_nova.endpoint
        nova_endpoint = None
        if nova_endpoint is None:
            nova_endpoint = keystone_client.service_catalog.url_for(
                service_type='compute',
                endpoint_type=endpoint_type
            )
        extensions = nc.discover_extensions(CONF.clients_nova.api_version)
        args = {
            'project_id': keystone_client.project_id,
            # nova client doesn't support v3 auth
            'auth_url': keystone_client.auth_url,
            'service_type': 'compute',
            'user_id': keystone_client.user_id,
            'extensions': extensions,
            'endpoint_type': CONF.clients_nova.endpoint_type,
            'bypass_url': nova_endpoint,
            'auth_token': keystone_client.auth_token
        }
        return nc.Client(
            CONF.clients_nova.api_version,
            **args
        )

    def get_machine(self, server):
        try:
            self._client.servers.find(name=server)
            exists = True
        except exceptions.NotFound as ex:
            exists = False
        return exists

    def deploy_machine(self, name, image):
        LOG.debug("Creating a nova client")
        args = {
            'name': name,
            'image': self._client.images.find(name=image),
            'flavor': self._client.flavors.find(name='m1.tiny'),
        }
        self._machine = self._client.servers.create(**args)

    def delete_machine(self, name):
        server = self._client.servers.find(name=name)
        server.delete()

    def get_ip(self):
        """Return the server's IP"""
        return self._client.servers.ips(self._machine)[0]
