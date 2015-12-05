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
from chef_validator.common import log as logging
from oslo_config import cfg

from chef_validator.common.exception \
    import AmbiguousNameException, \
    ImageNotFound

LOG = logging.getLogger(__name__)
opts = [
    cfg.StrOpt('api_version', default='2'),
    cfg.StrOpt('endpoint_type', default='publicURL'),
    cfg.StrOpt('endpoint'),
]
CONF = cfg.CONF
CONF.register_opts(opts, group="clients_nova")


class NovaClient(object):
    def __init__(self, context):
        self._client = self.create_nova_client(context)
        self._client.authenticate()
        self._machine = None

    def create_nova_client(self, context):
        api_version = CONF.clients_nova.api_version
        endpoint_type = CONF.clients_nova.endpoint_type
        nova_endpoint = CONF.clients_nova.endpoint
        args = {
            'tenant_id': context.tenant_id,
            'auth_url': context.auth_url,
            'service_type': 'compute',
            'user_id': context.user_id,
            'endpoint_type': endpoint_type,
            'bypass_url': nova_endpoint,
            'auth_token': context.auth_token
        }
        return nc.Client(
            api_version,
            **args
        )

    def list(self):
        images = self._client.images.list()
        # while True:
        #     try:
        #         image = images.next()
        #         yield self._format(image)
        #     except StopIteration:
        #         break
        return [self._format(i) for i in images]

    @staticmethod
    def _format(image):
        res = {"id": image.id, "name": image.name}
        return res

    def get_image_by_name(self, name):
        images = [i for i in self._client.images.list() if name == i.name]
        if len(images) == 0:
            raise ImageNotFound(name=name)
        elif len(images) > 1:
            raise AmbiguousNameException(name=name)
        else:
            return self._format(images[0])

    def get_machine(self, server):
        try:
            self._client.servers.find(name=server)
            exists = True
        except exceptions.NotFound:
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
        import time
        status = self._machine.status
        while status == 'BUILD':
            time.sleep(5)
            # Retrieve the instance again so the status field updates
            status = self._client.servers.get(self._machine.id).status

    def delete_machine(self, name):
        server = self._client.servers.find(name=name)
        server.delete()

    def get_ip(self):
        """Return the server's IP"""
        return self._client.servers.ips(self._machine)['public'][0]['addr']

    def get_serial(self):
        """return a serial console url"""
        return self._machine.get_serial_console('serial')
