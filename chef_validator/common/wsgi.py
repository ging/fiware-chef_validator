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

"""Utility methods for working with WSGI servers."""
import time
import errno
import logging as sys_logging
import routes
import routes.middleware
import webob.dec
import webob.exc

from oslo_service import service
from oslo_service import sslutils
from oslo_log import log as logging
import eventlet
eventlet.patcher.monkey_patch(all=False, socket=True)
import eventlet.wsgi
from eventlet.green import socket

from chef_validator.common import exceptions
from chef_validator.common.config import CONF

class WritableLogger(object):
    """A thin wrapper that responds to `write` and logs."""

    def __init__(self, LOG, level=sys_logging.DEBUG):
        self.LOG = LOG
        self.level = level

    def write(self, msg):
        self.LOG.log(self.level, msg.rstrip("\n"))

class Service(service.Service):
    """Provides a Service API for wsgi servers.

    This gives us the ability to launch wsgi servers with the
    Launcher classes in oslo_service.service.py.
    """

    def __init__(self, application, port,
                 host='0.0.0.0', backlog=4096, threads=1000):
        self.application = application
        self._port = port
        self._host = host
        self._backlog = backlog if backlog else CONF.backlog
        super(Service, self).__init__(threads)

    @staticmethod
    def _get_socket(host, port, backlog):
        info = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)[0]
        family = info[0]
        bind_addr = info[-1]

        sock = None
        retry_until = time.time() + 30
        while not sock and time.time() < retry_until:
            try:
                sock = eventlet.listen(bind_addr, backlog=backlog, family=family)
                if sslutils.is_enabled(CONF):
                    sock = sslutils.wrap(CONF, sock)

            except socket.error as err:
                if err.args[0] != errno.EADDRINUSE:
                    raise
                    eventlet.sleep(0.1)
        if not sock:
            raise RuntimeError(_("Could not bind to %(host)s:%(port)s after trying for 30 seconds") %
                               {'host': host, 'port': port})
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sockets can hang around forever without keepalive
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        # This option isn't available in the OS X version of eventlet
        if hasattr(socket, 'TCP_KEEPIDLE'):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, CONF.tcp_keepidle)

        return sock

    def start(self):
        """Start serving this service using the provided server instance.

        :returns: None

        """
        super(Service, self).start()
        self._socket = self._get_socket(self._host, self._port, self._backlog)
        self.tg.add_thread(self._run, self.application, self._socket)

    @property
    def backlog(self):
        return self._backlog

    @property
    def host(self):
        return self._socket.getsockname()[0] if self._socket else self._host

    @property
    def port(self):
        return self._socket.getsockname()[1] if self._socket else self._port

    def stop(self):
        """Stop serving this API.

        :returns: None

        """
        super(Service, self).stop()

    def reset(self):
        super(Service, self).reset()
        logging.setup(CONF, 'chef_validator')

    def _run(self, application, socket):
        """Start a WSGI server in a new green thread."""
        logger = logging.getLogger('eventlet.wsgi')
        eventlet.wsgi.server(socket, application, custom_pool=self.tg.pool, log=WritableLogger(logger))
