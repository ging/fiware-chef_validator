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
"""Main action mapper"""

from chef_validator.common import log as logging
from oslo_config import cfg
from webob import exc

from chef_validator.common import wsgi
from chef_validator.common.i18n import _LI, _
import chef_validator.common.utils
from chef_validator.engine.validate import ValidateEngine

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class ValidateController(object):
    """
    Validate Controller Object
    Implements Application logic
    """
    def __init__(self):
        self.ve = ValidateEngine()

    def validate(self, request, body):
        """Validate the given cookbook
        :param request: request context
        :param body: a json with deployment parameters
        :return : a json file with process results
        """
        body = body or {}
        if len(body) < 1:
            raise exc.HTTPBadRequest(_("No action specified"))
        try:
            cookbook = body['cookbook']
            image = body['image']
        except KeyError:
            raise exc.HTTPBadRequest(_("Insufficient payload"))

        if 'recipe' in body.keys():
            recipe = body['recipe']
        else:
            recipe = "default"
        LOG.info(
            _LI('Processing Request for cookbook {cookbook}, recipe {recipe}, '
                'image {image}').format(cookbook=cookbook, recipe=recipe,
                                        image=image))
        res = self.ve.validate_cookbook(
            cookbook, recipe, image, request
        )
        return res


def create_resource():
    """
    Actions action factory method.
    """
    deserializer = chef_validator.common.utils.JSONDeserializer()
    serializer = chef_validator.common.utils.JSONSerializer()
    return wsgi.Resource(ValidateController(), deserializer, serializer)
