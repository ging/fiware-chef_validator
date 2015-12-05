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

import glanceclient

from chef_validator.common import log as logging
from oslo_config import cfg

LOG = logging.getLogger(__name__)
opts = [
    cfg.IntOpt('api_version', default=2),
    cfg.StrOpt('endpoint_type', default='publicURL'),
    cfg.StrOpt('endpoint'),
]
CONF = cfg.CONF
CONF.register_opts(opts, group="clients_glance")


class GlanceClient(object):
    def __init__(self, ks):
        self.create_glance_client(ks)

    def list(self):
        images = self._client.images.list()
        while True:
            try:
                image = images.next()
                yield self._format(image)
            except StopIteration:
                break

    def get_by_name(self, name):
        images = list(self._client.images.list(filters={"name": name}))
        if len(images) > 1:
            raise AmbiguousNameException(name)
        elif len(images) == 0:
            return None
        else:
            return self._format(images[0])

    def getById(self, imageId):
        image = self._client.images.get(imageId)
        return self._format(image)

    @staticmethod
    def _format(image):
        res = {"id": image.id, "name": image.name}
        return res

    def create_glance_client(self, keystone_client):
        LOG.debug("Creating a glance client")
        glance_endpoint = CONF.clients_glance.endpoint
        if glance_endpoint is None:
            glance_endpoint = keystone_client.service_catalog.url_for(
                service_type='image',
                endpoint_type=CONF.clients_glance.endpoint_type
            )
        self._client = glanceclient.Client(
            CONF.clients_glance.api_version,
            endpoint=glance_endpoint,
            token=keystone_client.auth_token,
        )


class AmbiguousNameException(Exception):
    def __init__(self, name):
        super(AmbiguousNameException, self).__init__("Image name '%s'"
                                                     " is ambiguous" % name)
