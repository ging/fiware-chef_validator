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
Routines for configuring Chef Validator
"""
from __future__ import unicode_literals

from eventlet.green import socket

from oslo_config import cfg
from oslo_log import log as logging

from chef_validator.common.i18n import _
from chef_validator import version

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

bind_opts = [
    cfg.StrOpt('bind_host', default=socket.gethostname(), help=_('Name of the engine node.')),
    cfg.StrOpt('bind_port', default=4041, help=_('Listening port of the engine node.')),
]

CONF.register_cli_opts(bind_opts)


def parse_args(args=None, usage=None, default_config_files=None):
    CONF(args=args,
         project='chef_validator',
         version=version.version_string,
         usage=usage,
         default_config_files=default_config_files)
