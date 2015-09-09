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

from __future__ import unicode_literals
""" Tests for chef_validator.common.exception """

from chef_validator.tests.base import ValidatorTestCase
from chef_validator.common.exception import AuthorizationFailure
from chef_validator.common.exception import CookbookInstallException
from chef_validator.common.exception import OpenstackException
from chef_validator.common.exception import RecipeDeploymentException
from chef_validator.common.exception import MalformedRequestBody
from chef_validator.common.exception import HTTPExceptionDisguise
from chef_validator.common.exception import CookbookSyntaxException
from chef_validator.common.exception import SerialConnectException
from chef_validator.common.exception import NotAuthenticated
from chef_validator.common.exception import InvalidContentType
from chef_validator.common.exception import ImageNotFound
from chef_validator.common.exception import SshConnectException
from chef_validator.common.exception import DockerContainerException
from chef_validator.common.exception import AmbiguousNameException
from chef_validator.common.exception import EntityNotFound


def TestAuthorizationFailure(ValidatorTestCase):
    """ Tests for class AuthorizationFailure """
    pass

def TestCookbookInstallException(ValidatorTestCase):
    """ Tests for class CookbookInstallException """
    pass

def TestOpenstackException(ValidatorTestCase):
    """ Tests for class OpenstackException """
    pass

def TestRecipeDeploymentException(ValidatorTestCase):
    """ Tests for class RecipeDeploymentException """
    pass

def TestMalformedRequestBody(ValidatorTestCase):
    """ Tests for class MalformedRequestBody """
    pass

def TestHTTPExceptionDisguise(ValidatorTestCase):
    """ Tests for class HTTPExceptionDisguise """
    pass

def TestCookbookSyntaxException(ValidatorTestCase):
    """ Tests for class CookbookSyntaxException """
    pass

def TestSerialConnectException(ValidatorTestCase):
    """ Tests for class SerialConnectException """
    pass

def TestNotAuthenticated(ValidatorTestCase):
    """ Tests for class NotAuthenticated """
    pass

def TestInvalidContentType(ValidatorTestCase):
    """ Tests for class InvalidContentType """
    pass

def TestImageNotFound(ValidatorTestCase):
    """ Tests for class ImageNotFound """
    pass

def TestSshConnectException(ValidatorTestCase):
    """ Tests for class SshConnectException """
    pass

def TestDockerContainerException(ValidatorTestCase):
    """ Tests for class DockerContainerException """
    pass

def TestAmbiguousNameException(ValidatorTestCase):
    """ Tests for class AmbiguousNameException """
    pass

def TestEntityNotFound(ValidatorTestCase):
    """ Tests for class EntityNotFound """
    pass
