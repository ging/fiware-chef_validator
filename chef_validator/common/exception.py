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

_FATAL_EXCEPTION_FORMAT_ERRORS = False


class Error(Exception):
    def __init__(self, message=None):
        super(Error, self).__init__(message)


class OpenstackException(Exception):
    """Base Exception class.

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    msg_fmt = "An unknown exception occurred"

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


class InvalidContentType(OpenstackException):
    msg_fmt = "Invalid content type %(content_type)s"


class MalformedRequestBody(OpenstackException):
    msg_fmt = "Malformed message body: %(reason)s"


class AuthorizationFailure(OpenstackException):
    msg_fmt = "Authorization failed."


class TimeoutException(Exception):
    pass


class NotAuthenticated(OpenstackException):
    msg_fmt = "Authentication failed."


class ImageNotFound(OpenstackException):
    msg_fmt = "The requested Image doesn't exist for the given user"


class NotFound(OpenstackException):
    def __init__(self, msg_fmt='Not found'):
        self.msg_fmt = msg_fmt
        super(NotFound, self).__init__()


class EntityNotFound(OpenstackException):
    msg_fmt = "The %(entity)s (%(name)s) could not be found."


# Chef exceptions
class SshConnectException(OpenstackException):
    msg_fmt = "The SSH connection to %(host)s could not be stablished."


class CookbookInstallException(OpenstackException):
    msg_fmt = "Error installing cookbook %(recipe)s"


class CookbookSyntaxException(OpenstackException):
    msg_fmt = "The provided cookbook syntax is incorrect for %(recipe)s"


class RecipeDeploymentException(OpenstackException):
    msg_fmt = "Error deploying the provided recipe: %(recipe)s"
