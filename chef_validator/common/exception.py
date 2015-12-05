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
import sys
from chef_validator.common.i18n import _

_FATAL_EXCEPTION_FORMAT_ERRORS = False


class OpenstackException(Exception):
    """Base Exception class.

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    msg_fmt = _("An unknown exception occurred")

    def __init__(self, **kwargs):
        try:
            self._error_string = self.msg_fmt % kwargs

        except Exception:
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise
            else:
                self._error_string = self.msg_fmt

    def __str__(self):
        return self._error_string


class HTTPExceptionDisguise(Exception):
    """Disguises HTTP exceptions so they can be handled by the webob fault
    application in the wsgi pipeline.
    """

    def __init__(self, exception):
        self.exc = exception
        self.tb = sys.exc_info()[2]


class InvalidContentType(OpenstackException):
    msg_fmt = _("Invalid content type %(content_type)s")


class MalformedRequestBody(OpenstackException):
    msg_fmt = _("Malformed message body: %(reason)s")


class AuthorizationFailure(OpenstackException):
    msg_fmt = _("Authorization failed.")


class NotAuthenticated(OpenstackException):
    msg_fmt = _("Authentication failed.")


class EntityNotFound(OpenstackException):
    msg_fmt = _("The %(entity)s (%(name)s) could not be found.")


# Image exceptions
class ImageNotFound(OpenstackException):
    msg_fmt = _("The Image %(name)s doesn't exist for the given user")


class AmbiguousNameException(OpenstackException):
    msg_fmt = _("Image name %(name)s is ambiguous")


# Chef exceptions
class SshConnectException(OpenstackException):
    msg_fmt = _("The SSH connection to %(host)s could not be stablished.")


class SerialConnectException(OpenstackException):
    msg_fmt = _("The Serial connection to %(host)s could not be stablished.")


class CookbookInstallException(OpenstackException):
    msg_fmt = _("Error installing cookbook %(cookbook)s")


class CookbookSyntaxException(OpenstackException):
    msg_fmt = _("The provided cookbook syntax is incorrect for "
                "cookbook: %(cookbook)s")


class CookbookDeploymentException(OpenstackException):
    msg_fmt = _("Error deploying the provided cookbook: %(cookbook)s")


class DockerContainerException(OpenstackException):
    msg_fmt = _("Error deploying the provided image: %(image)s")
