#!/usr/bin/env python
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
"""A very simple example client for Chef Validator"""

import json
import pprint
import os
import sys
from eventlet.green import urllib2
from oslo_config import cfg

# If ../chef_validator/__init__.py exists, add ../ to Python search path,
# so that it will override what happens to be installed in
# /usr/(local/)lib/python...
root = os.path.abspath(
    os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir)
)
if os.path.exists(os.path.join(root, 'chef_validator', '__init__.py')):
    sys.path.insert(0, root)

# simple local logging
from chef_validator.common import log as logging

LOG = logging.getLogger(__name__)

cfg.CONF.debug = True
cfg.CONF.logging_default_format_string = \
    "%(levelname)s (%(module)s:%(lineno)d) %(message)s"
logging.setup(cfg.CONF, 'chef_validator_client')

# local configuration
opts = [
    cfg.StrOpt('image', help="Glance Image to deploy"),
    cfg.StrOpt('cookbook', help="Name of the cookbook to deploy"),
    cfg.StrOpt('username', help="Keystone username"),
    cfg.StrOpt('password', help="Keystone password"),
    cfg.StrOpt('validator_url', help="Chef Validator Url"),
]
cfg.CONF.register_cli_opts(opts)
cfg.CONF(sys.argv[1:])
CONF = cfg.CONF

# default values
USERNAME = os.environ.get('OS_USERNAME', CONF.username)
PASSWORD = os.environ.get('OS_PASSWORD', CONF.password)
VALIDATOR_URL = os.environ.get('CHEF_VALIDATOR_URL', CONF.validator_url)


def client():
    """Sends static request based on cmdline arguments, logs the response"""
    if USERNAME is None \
            or PASSWORD is None \
            or VALIDATOR_URL is None \
            or not VALIDATOR_URL.endswith("validate"):
        raise Exception("Needed valid username, password and validator_url")
    # sample request data
    postdata = {
        "cookbook": CONF.cookbook,
        "image": CONF.image
    }

    # sends the request
    req = urllib2.Request(VALIDATOR_URL)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-User', USERNAME)
    req.add_header('X-Auth-Key', PASSWORD)
    data = json.dumps(postdata)
    try:
        response = urllib2.urlopen(req, data)
        data = response.read()
        data = json.loads(data)
    except urllib2.HTTPError as e:
        data = e.read()
    pprint.pprint(data)


if __name__ == '__main__':
    client()
