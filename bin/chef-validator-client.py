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
""" A very simple example client for Chef Validator """

import json
import logging
import os
import sys

from eventlet.green import urllib2

from oslo_config import cfg

opts = [
    cfg.StrOpt('image', help="Glance Image to deploy"),
    cfg.StrOpt('recipe', help="Name of the recipe to deploy"),
    cfg.StrOpt('username', help="Keystone username"),
    cfg.StrOpt('password', help="Keystone password"),
    cfg.StrOpt('validator_url', help="Chef Validator Url"),
]

cfg.CONF.register_cli_opts(opts)
cfg.CONF(sys.argv[1:])

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DEBUG = True
USERNAME = os.environ.get('OS_USERNAME', CONF.username)
PASSWORD = os.environ.get('OS_PASSWORD', CONF.password)
VALIDATOR_URL = os.environ.get('CHEF_VALIDATOR_URL', CONF.validator_url)


def client():
    """ Sends a static request based on commandline arguments,
    logs the response """
    log_lvl = logging.DEBUG if DEBUG else logging.WARNING
    logging.basicConfig(
        format="%(levelname)s (%(module)s:%(lineno)d) %(message)s",
        level=log_lvl)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
    postdata = {
        "recipe": CONF.recipe,
        "image": CONF.image
    }
    # sends the request
    req = urllib2.Request(VALIDATOR_URL)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-User', USERNAME)
    req.add_header('X-Auth-Key', PASSWORD)
    data = json.dumps(postdata)
    response = urllib2.urlopen(req, data)
    data = response.read()
    LOG.info(data)


if __name__ == '__main__':
    client()
