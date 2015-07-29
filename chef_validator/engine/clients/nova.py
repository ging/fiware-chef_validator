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

from chef_validator.common import exception
from chef_validator.common.i18n import _LW

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
        import pprint
        pprint.pprint(keystone_client.__dict__)
        LOG.debug("Creating a nova client")
        endpoint_type = CONF.clients_nova.endpoint_type
        nova_endpoint = CONF.clients_nova.endpoint
        if nova_endpoint is None:
            nova_endpoint = keystone_client.service_catalog.url_for(
                service_type='compute',
                endpoint_type=endpoint_type
            )
        extensions = nc.discover_extensions(CONF.clients_nova.api_version)
        args = {
            'project_id': keystone_client.project_id,
            'auth_url': keystone_client.auth_url,
            'service_type': 'compute',
            'user_id': keystone_client.user_id,
            'extensions': extensions,
            'endpoint_type': CONF.clients_nova.endpoint_type,
            'endpoint': nova_endpoint.replace("/v3", "/"),
            'username': 'demo',
            'auth_token': keystone_client.auth_token
        }
        return nc.Client(
            CONF.clients_nova.api_version,
            **args
        )

    def get_server(self, server):
        try:
            return self._client.servers.get(server)
        except exceptions.NotFound as ex:
            LOG.warn(_LW('Server (%(server)s) not found: %(ex)s'),
                     {'server': server, 'ex': ex})
            raise exception.EntityNotFound(entity='Server', name=server)

    def create_server(self, image):
        print self._client.images.list()
        # self._machine = self._client.servers.create(
        #     name=image['name'],
        #     image=image['id'],
        #     flavor='m1.nano'
        # )
