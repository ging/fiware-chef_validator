#!/usr/bin/python
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

"""
Chef Validator API Server. An OpenStack ReST API to Validate Chef Cookbooks.
"""

import os
import sys
import six
import oslo_i18n as i18n
from oslo_config import cfg

if 'config_dir' not in cfg.CONF:
    cfg.CONF.config_dir = "/etc/chef_validator"

# If ../chef_validator/__init__.py exists, add ../ to Python search path,
# so that it will override what happens to be installed in
# /usr/(local/)lib/python...
root = os.path.abspath(
    os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir)
)
if os.path.exists(os.path.join(root, 'chef_validator', '__init__.py')):
    sys.path.insert(0, root)

from chef_validator.common import log as logging
from chef_validator.common.i18n import _LI
from chef_validator.common import config
from chef_validator.common import wsgi

i18n.enable_lazy()

LOG = logging.getLogger()
CONF = config.CONF


def main():
    """Launch validator API """
    try:
        config.parse_args()
        logging.setup(CONF, 'chef_validator_api')
        app = config.load_paste_app("chef_validator_api")
        port, host = (CONF.bind_port, CONF.bind_host)
        LOG.info(_LI('Starting Chef Validator ReST API on %(host)s:%(port)s'),
                 {'host': host, 'port': port})
        server = wsgi.Service(app, port, host)
        server.start()
        server.wait()
    except RuntimeError as e:
        msg = six.text_type(e)
        sys.exit("ERROR: %s" % msg)


if __name__ == '__main__':
    main()
