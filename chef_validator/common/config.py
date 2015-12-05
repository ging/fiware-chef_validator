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

import os

from eventlet.green import socket
from oslo_config import cfg
from chef_validator.common import log as logging

from chef_validator.common import wsgi
from chef_validator.common.i18n import _
from chef_validator.tests.unit import version

socket_opts = [
    cfg.IntOpt('tcp_keepidle',
               default=600,
               help="Sets the value of TCP_KEEPIDLE in seconds for each "
                    "server socket. Not supported on OS X."),
]

CONF = cfg.CONF
CONF.register_opts(socket_opts)
LOG = logging.getLogger(__name__)

# Local ip/port binding options
bind_opts = [
    cfg.StrOpt('bind_host', default=socket.gethostname(),
               help=_('Name of the engine node.')),
    cfg.StrOpt('bind_port', default=4041,
               help=_('Listening port of the engine node.')),
]
CONF.register_cli_opts(bind_opts)

# Paste/Deploy server options
paste_deploy_group = cfg.OptGroup('paste_deploy')
paste_deploy_opts = [
    cfg.StrOpt('config_file', default="api-paste.ini",
               help=_("The API config file to use.")),
    cfg.StrOpt('flavor', help=_("The flavor to use."))
]
CONF.register_group(paste_deploy_group)
CONF.register_opts(paste_deploy_opts, group='paste_deploy')

# Baseline client options
clients_opts = [
    cfg.StrOpt('endpoint_type',
               default='publicURL',
               help=_(
                   'Type of endpoint in Identity service catalog to use '
                   'for communication with the OpenStack service.')),
]
CONF.register_opts(clients_opts)


def parse_args(args=None, usage=None, default_config_files=None):
    CONF(args=args,
         project='chef_validator',
         version=version.version_string,
         usage=usage,
         default_config_files=default_config_files)


def _get_deployment_flavor():
    """Retrieve the paste_deploy.flavor config item, formatted appropriately
       for appending to the application name.
    """
    flavor = CONF.paste_deploy.flavor
    return '' if not flavor else ('-' + flavor)


def _get_paste_config_path():
    paste_suffix = '-paste.ini'
    conf_suffix = '.conf'
    if CONF.config_file:
        # Assume paste config is in a paste.ini file corresponding
        # to the last config file
        path = CONF.config_file[-1].replace(conf_suffix, paste_suffix)
    else:
        path = CONF.prog + '-paste.ini'
    return CONF.find_file(os.path.basename(path))


def _get_deployment_config_file():
    """Retrieve the deployment_config_file config item, formatted as an
       absolute pathname.
    """
    path = CONF.paste_deploy.config_file
    if CONF.debug:
        return os.path.abspath(os.path.join(CONF.config_dir, path))
    if not path:
        path = _get_paste_config_path()
    if not path:
        msg = _("Unable to locate paste config file for %s.") % CONF.prog
        raise RuntimeError(msg)
    return os.path.abspath(path)


def load_paste_app(app_name=None):
    """Builds and returns a WSGI app from a paste config file.

    We assume the last config file specified in the supplied ConfigOpts
    object is the paste config file.

    :param app_name: name of the application to load

    :raises RuntimeError when config file cannot be located or application
            cannot be loaded from config file
    """
    if app_name is None:
        app_name = CONF.prog

    app_name += _get_deployment_flavor()
    conf_file = _get_deployment_config_file()
    if conf_file is None:
        raise RuntimeError(_("Unable to locate config file"))

    try:
        LOG.debug("Loading %(app_name)s from %(conf_file)s" %
                  {'conf_file': conf_file, 'app_name': app_name})
        app = wsgi.paste_deploy_app(conf_file, app_name, cfg.CONF)
        return app
    except (LookupError, ImportError) as e:
        msg = _("Unable to load %(app_name)s from configuration file "
                "%(conf_file)s. \nGot: %(e)r") % \
            {'conf_file': conf_file, 'app_name': app_name, 'e': e}
        LOG.error(msg)
        raise RuntimeError(msg)
