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
"""Tests for chef_validator.common.exception """
from __future__ import unicode_literals
from chef_validator.common.exception import AuthorizationFailure
from chef_validator.common.exception import CookbookInstallException
from chef_validator.common.exception import OpenstackException
from chef_validator.common.exception import CookbookDeploymentException
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
from chef_validator.tests.unit.base import ValidatorTestCase


class AuthorizationFailureTestCase(ValidatorTestCase):
    """Tests for class AuthorizationFailure """

    def setUp(self):
        """Create a AuthorizationFailure instance """
        super(AuthorizationFailureTestCase, self).setUp()
        self.item = AuthorizationFailure()

    def tearDown(self):
        """Cleanup the AuthorizationFailure instance """
        super(AuthorizationFailureTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class CookbookInstallExceptionTestCase(ValidatorTestCase):
    """Tests for class CookbookInstallException """

    def setUp(self):
        """Create a CookbookInstallException instance """
        super(CookbookInstallExceptionTestCase, self).setUp()
        self.item = CookbookInstallException()

    def tearDown(self):
        """Cleanup the CookbookInstallException instance """
        super(CookbookInstallExceptionTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class OpenstackExceptionTestCase(ValidatorTestCase):
    """Tests for class OpenstackException """

    def setUp(self):
        """Create a OpenstackException instance """
        super(OpenstackExceptionTestCase, self).setUp()
        self.item = OpenstackException()

    def tearDown(self):
        """Cleanup the OpenstackException instance """
        super(OpenstackExceptionTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class CookbookDeploymentExceptionTestCase(ValidatorTestCase):
    """Tests for class CookbookDeploymentException """

    def setUp(self):
        """Create a CookbookDeploymentException instance """
        super(CookbookDeploymentExceptionTestCase, self).setUp()
        self.item = CookbookDeploymentException()

    def tearDown(self):
        """Cleanup the CookbookDeploymentException instance """
        super(CookbookDeploymentExceptionTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class MalformedRequestBodyTestCase(ValidatorTestCase):
    """Tests for class MalformedRequestBody """

    def setUp(self):
        """Create a MalformedRequestBody instance """
        super(MalformedRequestBodyTestCase, self).setUp()
        self.item = MalformedRequestBody()

    def tearDown(self):
        """Cleanup the MalformedRequestBody instance """
        super(MalformedRequestBodyTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class HTTPExceptionDisguiseTestCase(ValidatorTestCase):
    """Tests for class HTTPExceptionDisguise """

    def setUp(self):
        """Create a HTTPExceptionDisguise instance """
        super(HTTPExceptionDisguiseTestCase, self).setUp()
        self.item = HTTPExceptionDisguise()

    def tearDown(self):
        """Cleanup the HTTPExceptionDisguise instance """
        super(HTTPExceptionDisguiseTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class CookbookSyntaxExceptionTestCase(ValidatorTestCase):
    """Tests for class CookbookSyntaxException """

    def setUp(self):
        """Create a CookbookSyntaxException instance """
        super(CookbookSyntaxExceptionTestCase, self).setUp()
        self.item = CookbookSyntaxException()

    def tearDown(self):
        """Cleanup the CookbookSyntaxException instance """
        super(CookbookSyntaxExceptionTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class SerialConnectExceptionTestCase(ValidatorTestCase):
    """Tests for class SerialConnectException """

    def setUp(self):
        """Create a SerialConnectException instance """
        super(SerialConnectExceptionTestCase, self).setUp()
        self.item = SerialConnectException()

    def tearDown(self):
        """Cleanup the SerialConnectException instance """
        super(SerialConnectExceptionTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class NotAuthenticatedTestCase(ValidatorTestCase):
    """Tests for class NotAuthenticated """

    def setUp(self):
        """Create a NotAuthenticated instance """
        super(NotAuthenticatedTestCase, self).setUp()
        self.item = NotAuthenticated()

    def tearDown(self):
        """Cleanup the NotAuthenticated instance """
        super(NotAuthenticatedTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class InvalidContentTypeTestCase(ValidatorTestCase):
    """Tests for class InvalidContentType """

    def setUp(self):
        """Create a InvalidContentType instance """
        super(InvalidContentTypeTestCase, self).setUp()
        self.item = InvalidContentType()

    def tearDown(self):
        """Cleanup the InvalidContentType instance """
        super(InvalidContentTypeTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class ImageNotFoundTestCase(ValidatorTestCase):
    """Tests for class ImageNotFound """

    def setUp(self):
        """Create a ImageNotFound instance """
        super(ImageNotFoundTestCase, self).setUp()
        self.item = ImageNotFound()

    def tearDown(self):
        """Cleanup the ImageNotFound instance """
        super(ImageNotFoundTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class SshConnectExceptionTestCase(ValidatorTestCase):
    """Tests for class SshConnectException """

    def setUp(self):
        """Create a SshConnectException instance """
        super(SshConnectExceptionTestCase, self).setUp()
        self.item = SshConnectException()

    def tearDown(self):
        """Cleanup the SshConnectException instance """
        super(SshConnectExceptionTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class DockerContainerExceptionTestCase(ValidatorTestCase):
    """Tests for class DockerContainerException """

    def setUp(self):
        """Create a DockerContainerException instance """
        super(DockerContainerExceptionTestCase, self).setUp()
        self.item = DockerContainerException()

    def tearDown(self):
        """Cleanup the DockerContainerException instance """
        super(DockerContainerExceptionTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class AmbiguousNameExceptionTestCase(ValidatorTestCase):
    """Tests for class AmbiguousNameException """

    def setUp(self):
        """Create a AmbiguousNameException instance """
        super(AmbiguousNameExceptionTestCase, self).setUp()
        self.item = AmbiguousNameException()

    def tearDown(self):
        """Cleanup the AmbiguousNameException instance """
        super(AmbiguousNameExceptionTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()


class EntityNotFoundTestCase(ValidatorTestCase):
    """Tests for class EntityNotFound """

    def setUp(self):
        """Create a EntityNotFound instance """
        super(EntityNotFoundTestCase, self).setUp()
        self.item = EntityNotFound()

    def tearDown(self):
        """Cleanup the EntityNotFound instance """
        super(EntityNotFoundTestCase, self).tearDown()
        self.m.UnsetStubs()
        self.m.ResetAll()
