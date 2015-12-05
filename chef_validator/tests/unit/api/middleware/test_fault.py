# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import inspect
import re
import six
from oslo_config import cfg
from chef_validator.common import log
from oslo_messaging._drivers import common as rpc_common
import webob
import chef_validator.api.middleware.fault as fault
from chef_validator.common import exception as chef_validator_exc
from chef_validator.common.i18n import _
from chef_validator.tests.unit.base import ValidatorTestCase


class StackNotFoundChild(chef_validator_exc.EntityNotFound):
    pass


class ErrorWithNewline(webob.exc.HTTPBadRequest):
    pass


class FaultMiddlewareTest(ValidatorTestCase):
    def setUp(self):
        super(FaultMiddlewareTest, self).setUp()

    def test_disguised_http_exception_with_newline(self):
        wrapper = fault.FaultWrapper(None)
        newline_error = ErrorWithNewline('Error with \n newline')
        msg = wrapper._error(chef_validator_exc.HTTPExceptionDisguise(
            newline_error)
        )
        error = {'code': 400,
                 'error': {'message': 'Error with \n newline',
                           'traceback': None,
                           'type': 'ErrorWithNewline'},
                 'explanation': ('The server could not comply with the '
                                 'request since it is either malformed '
                                 'or otherwise incorrect.'),
                 'title': 'Bad Request'}
        expected = {
            'success': False,
            'response': error,
            'install': {
                'success': False,
                'response': ''
            },
            'test': {
                'success': False,
                'response': ''
            },
            'deploy': {
                'success': False,
                'response': ''
            }
        }
        self.assertEqual(expected, msg)

    def test_http_exception_with_traceback(self):
        wrapper = fault.FaultWrapper(None)
        newline_error = ErrorWithNewline(
            'Error with \n newline\nTraceback (most recent call last):\nFoo')
        msg = wrapper._error(chef_validator_exc.HTTPExceptionDisguise(
            newline_error)
        )
        error = {u'code': 400,
                 u'error':
                     {u'message': u'Error with \n newline',
                      u'traceback': u'Traceback (most recent call last):\nFoo',
                      u'type': 'ErrorWithNewline'},
                 u'explanation':
                     'The server could not comply with the request since it '
                     'is either malformed or otherwise incorrect.',
                 u'title': 'Bad Request'}
        expected = {
            'success': False,
            'response': error,
            'install': {
                'success': False,
                'response': ''
            },
            'test': {
                'success': False,
                'response': ''
            },
            'deploy': {
                'success': False,
                'response': ''
            }
        }
        self.assertEqual(expected, msg)

    def test_openstack_exception_with_kwargs(self):
        wrapper = fault.FaultWrapper(None)
        msg = wrapper._error(chef_validator_exc.InvalidContentType(
            content_type='a')
        )
        error = {u'code': 500,
                 u'error': {u'message': u'Invalid content type a',
                            u'traceback': 'None\n',
                            u'type': 'InvalidContentType'},
                 u'explanation': 'The server has either erred or is incapable '
                                 'of performing the requested operation.',
                 u'title': 'Internal Server Error'}
        expected = {
            'success': False,
            'response': error,
            'install': {
                'success': False,
                'response': ''
            },
            'test': {
                'success': False,
                'response': ''
            },
            'deploy': {
                'success': False,
                'response': ''
            }
        }
        self.assertEqual(expected, msg)

    def test_openstack_exception_without_kwargs(self):
        wrapper = fault.FaultWrapper(None)
        msg = wrapper._error(chef_validator_exc.OpenstackException())
        error = {u'code': 500,
                 u'error': {u'message': u'An unknown exception occurred',
                            u'traceback': 'None\n',
                            u'type': 'OpenstackException'},
                 u'explanation': 'The server has either erred or is incapable '
                                 'of performing the requested operation.',
                 u'title': 'Internal Server Error'}
        expected = {
            'success': False,
            'response': error,
            'install': {
                'success': False,
                'response': ''
            },
            'test': {
                'success': False,
                'response': ''
            },
            'deploy': {
                'success': False,
                'response': ''
            }
        }
        self.assertEqual(expected, msg)

    def test_exception_with_non_ascii_chars(self):
        # We set debug to true to test the code path for serializing traces too
        cfg.CONF.set_override('debug', True)
        msg = u'Error with non-ascii chars \x80'

        class TestException(chef_validator_exc.OpenstackException):
            msg_fmt = msg

        wrapper = fault.FaultWrapper(None)
        msg = wrapper._error(TestException())
        error = {'code': 500,
                 'error': {'message': u'Error with non-ascii chars \x80',
                           'traceback': 'None\n',
                           'type': 'TestException'},
                 'explanation': ('The server has either erred or is '
                                 'incapable of performing the requested '
                                 'operation.'),
                 'title': 'Internal Server Error'}
        expected = {
            'success': False,
            'response': error,
            'install': {
                'success': False,
                'response': ''
            },
            'test': {
                'success': False,
                'response': ''
            },
            'deploy': {
                'success': False,
                'response': ''
            }
        }
        self.assertEqual(expected, msg)

    def test_remote_exception(self):
        # We want tracebacks
        cfg.CONF.set_override('debug', True)
        error = chef_validator_exc.InvalidContentType(content_type='a')
        exc_info = (type(error), error, None)
        serialized = rpc_common.serialize_remote_exception(exc_info)
        remote_error = rpc_common.deserialize_remote_exception(
            serialized, ["chef_validator.common.exception"])
        wrapper = fault.FaultWrapper(None)
        msg = wrapper._error(remote_error)
        expected_message, expected_traceback = six.text_type(
            remote_error).split('\n', 1)
        error = {u'code': 500,
                 u'error': {
                     u'message': u'Invalid content type %(content_type)s',
                     u'traceback': u'InvalidContentType: Invalid content '
                                   u'type a\n',
                     u'type': 'InvalidContentType'},
                 u'explanation': 'The server has either erred or is '
                                 'incapable of performing the requested '
                                 'operation.',
                 u'title': 'Internal Server Error'}
        expected = {
            'success': False,
            'response': error,
            'install': {
                'success': False,
                'response': ''
            },
            'test': {
                'success': False,
                'response': ''
            },
            'deploy': {
                'success': False,
                'response': ''
            }
        }
        self.assertEqual(expected, msg)

    def remote_exception_helper(self, name, error):
        exc_info = (type(error), error, None)

        serialized = rpc_common.serialize_remote_exception(exc_info)
        remote_error = rpc_common.deserialize_remote_exception(
            serialized, name)
        wrapper = fault.FaultWrapper(None)
        msg = wrapper._error(remote_error)
        print msg
        errmsg = {
            'code': 500,
            'error': {'message': msg['response']['error']['message'],
                      'traceback': None,
                      'type': 'RemoteError'},
            'explanation': msg['response']['explanation'],
            'title': 'Internal Server Error'}
        expected = {
            'success': False,
            'response': errmsg,
            'install': {
                'success': False,
                'response': ''
            },
            'test': {
                'success': False,
                'response': ''
            },
            'deploy': {
                'success': False,
                'response': ''
            }
        }
        self.assertEqual(expected, msg)

    def test_all_remote_exceptions(self):
        for name, obj in inspect.getmembers(
                chef_validator_exc, lambda x: inspect.isclass(x) and
                issubclass(x, chef_validator_exc.OpenstackException)):
            if '__init__' in obj.__dict__:
                if obj == chef_validator_exc.OpenstackException:  #
                    # manually ignore baseclass
                    continue
                elif obj == chef_validator_exc.Error:
                    error = obj('Error')
                elif obj == chef_validator_exc.NotFound:
                    error = obj()
                elif obj == chef_validator_exc.ResourceFailure:
                    exc = chef_validator_exc.Error(_('Error'))
                    error = obj(exc, None, 'CREATE')
                elif obj == chef_validator_exc.ResourcePropertyConflict:
                    error = obj('%s' % 'a test prop')
                else:
                    continue
                self.remote_exception_helper(name, error)
                continue

            if hasattr(obj, 'msg_fmt'):
                kwargs = {}
                spec_names = re.findall('%\((\w+)\)([cdeEfFgGinorsxX])',
                                        obj.msg_fmt)

                for key, convtype in spec_names:
                    if convtype == 'r' or convtype == 's':
                        kwargs[key] = '"' + key + '"'
                    else:
                        # this is highly unlikely
                        raise Exception("test needs additional conversion"
                                        " type added due to %s exception"
                                        " using '%c' specifier" % (obj,
                                                                   convtype))

                error = obj(**kwargs)
                self.remote_exception_helper(name, error)

    def test_should_not_ignore_parent_classes(self):
        wrapper = fault.FaultWrapper(None)

        msg = wrapper._error(StackNotFoundChild(stack_name='a'))
        error = {u'code': 404,
                 u'error': {u'message': u'The %(entity)s (%(name)s) could '
                                        u'not be found.',
                            u'traceback': 'None\n',
                            u'type': 'StackNotFoundChild'},
                 u'explanation': 'The resource could not be found.',
                 u'title': 'Not Found'}
        expected = {
            'success': False,
            'response': error,
            'install': {
                'success': False,
                'response': ''
            },
            'test': {
                'success': False,
                'response': ''
            },
            'deploy': {
                'success': False,
                'response': ''
            }
        }
        self.assertEqual(expected, msg)

    def test_internal_server_error_when_exeption_and_parents_not_mapped(self):
        wrapper = fault.FaultWrapper(None)

        class NotMappedException(Exception):
            pass

        msg = wrapper._error(NotMappedException('A message'))
        error = {u'code': 500,
                 u'error': {u'message': u'A message',
                            u'traceback': 'None\n',
                            u'type': 'NotMappedException'},
                 u'explanation': 'The server has either erred or is incapable '
                                 'of performing the requested operation.',
                 u'title': 'Internal Server Error'}
        expected = {
            'success': False,
            'response': error,
            'install': {
                'success': False,
                'response': ''
            },
            'test': {
                'success': False,
                'response': ''
            },
            'deploy': {
                'success': False,
                'response': ''
            }
        }
        self.assertEqual(expected, msg)

    def test_should_not_ignore_parent_classes_even_for_remote_ones(self):
        # We want tracebacks
        cfg.CONF.set_override('debug', True)

        error = StackNotFoundChild(stack_name='a')
        exc_info = (type(error), error, None)
        serialized = rpc_common.serialize_remote_exception(exc_info)
        remote_error = rpc_common.deserialize_remote_exception(
            serialized, ["chef_validator.tests.test_fault_middleware"])

        wrapper = fault.FaultWrapper(None)
        msg = wrapper._error(remote_error)
        expected_message, expected_traceback = six.text_type(
            remote_error).split('\n', 1)
        error = {u'code': 500,
                 u'error': {
                     u'message': u"Remote error: StackNotFoundChild "
                                 u"The %(entity)s (%(name)s) could not be "
                                 u"found.\n[u'StackNotFoundChild: "
                                 u"The %(entity)s (%(name)s) "
                                 u"could not be found.\\n'].",
                     u'traceback': 'None\n',
                     u'type': 'RemoteError'},
                 u'explanation': 'The server has either erred or is incapable '
                                 'of performing the requested operation.',
                 u'title': 'Internal Server Error'}
        expected = {
            'success': False,
            'response': error,
            'install': {
                'success': False,
                'response': ''
            },
            'test': {
                'success': False,
                'response': ''
            },
            'deploy': {
                'success': False,
                'response': ''
            }
        }
        self.assertEqual(expected, msg)
