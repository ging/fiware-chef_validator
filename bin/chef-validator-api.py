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
from __future__ import unicode_literals
import os
import sys
import six

import oslo_i18n as i18n
from oslo_log import log as logging


from chef_validator.common.i18n import _LI

# If ../chef_validator/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
root = os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir)
if os.path.exists(os.path.join(root, 'chef_validator', '__init__.py')):
    sys.path.insert(0, root)

i18n.enable_lazy()

LOG = logging.getLogger('chef_validator.api')

if __name__ == '__main__':
    try:
        # logging.register_options(None)
        # logging.setup(None, 'chef_validator_api')
        LOG.info(_LI('Starting Chef Validator Rest API'))
    except RuntimeError as e:
        msg = six.text_type(e)
        sys.exit("ERROR: %s" % msg)
