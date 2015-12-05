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


from chef_validator.common import log as logging
from oslo_config import cfg
from chef_validator.common.exception import \
    SshConnectException, CookbookSyntaxException, \
    CookbookDeploymentException, CookbookInstallException
from chef_validator.common.i18n import _LW

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('username'),
    cfg.StrOpt('password'),
    cfg.StrOpt('cmd_install'),
    cfg.StrOpt('cmd_config'),
    cfg.StrOpt('cmd_inject'),
    cfg.StrOpt('cmd_test'),
    cfg.StrOpt('cmd_launch')
]
CONF = cfg.CONF
CONF.register_opts(opts, group="clients_chef")

# todo stub for pycrypto dependencies on win
import os

if 'nt' in os.name:
    class SSHClient(object):
        """SSHClient stub"""

        @staticmethod
        def set_missing_host_key_policy(dummy):
            """set_missing_host_key_policy stub
            :param dummy:
            """
            pass

        def disconnect(self):
            pass

    class AutoAddPolicy(object):
        """AutoAddPolicy stub"""
        pass
else:
    from paramiko import SSHClient, AutoAddPolicy


class ChefClientSSH(object):
    """Chef client wrapper"""

    def __init__(
            self,
            ip,
            user=CONF.clients_chef.username,
            passw=CONF.clients_chef.password
    ):
        """
        set internal parameters
        :param ip: remote machine ip
        :param user: remote machine user account name
        :param passw: remote machine user account password
        """
        self._ip = ip
        self._username = user
        self._password = passw
        self.ssh = SSHClient()

    def cookbook_deploy_test(self, cookbook):
        """Try to deploy the given cookbook through an serial connection
        :param cookbook: cookbook to deploy
        :return: dict message with results
        """
        LOG.debug("Sending cookbook to %s" % self._ip)
        b_success = True
        msg = {}
        self.connect_session()
        msg['install'] = self.run_install(cookbook)
        b_success &= msg['install']['success']
        msg['test'] = self.run_test(cookbook)
        b_success &= msg['test']['success']
        msg['deploy'] = self.run_deploy(cookbook)
        b_success &= msg['deploy']['success']

        # check execution output
        if b_success:
            msg['result'] = {
                'success': True,
                'result': "Cookbook %s successfully deployed\n" % cookbook
            }
        else:
            msg['result'] = {
                'success': False,
                'result': "Error deploying cookbook {}\n".format(cookbook)
            }
            LOG.error(_LW("%s") % msg)
        self.disconnect_session()
        return msg

    def run_deploy(self, cookbook):
        """Run cookbook deployment
        :param cookbook: cookbook to deploy
        :return msg: dictionary with results and state
        """
        try:
            # inject custom solo.json file
            json_cont = CONF.clients_chef.cmd_config.format(cookbook)
            cmd_inject = CONF.clients_chef.cmd_inject.format(json_cont)
            self.execute_command(cmd_inject)
            # launch execution
            cmd_launch = CONF.clients_chef.cmd_launch
            resp_launch = self.execute_command(cmd_launch)
            msg = {
                'success': True,
                'response': resp_launch
            }
            if resp_launch is None or "FATAL" in resp_launch:
                msg['success'] = False
        except Exception as e:
            self.disconnect_session()
            LOG.error(_LW("Cookbook deployment exception %s") % e)
            raise CookbookDeploymentException(cookbook=cookbook)
        return msg

    def run_test(self, cookbook):
        """Test cookbook syntax
        :param cookbook: cookbook to test
        :return msg: dictionary with results and state
        """
        try:
            cmd_test = CONF.clients_chef.cmd_test.format(cookbook)
            resp_test = self.execute_command(cmd_test)
            msg = {
                'success': True,
                'response': resp_test
            }
            for line in resp_test.splitlines():
                if "ERROR" in line:
                    msg['success'] = False
        except Exception as e:
            self.disconnect_session()
            LOG.error(_LW("Cookbook syntax exception %s") % e)
            raise CookbookSyntaxException(cookbook=cookbook)
        return msg

    def run_install(self, cookbook):
        """Run download and install command
        :param cookbook: cookbook to process
        :return msg: operation result
        """
        try:
            cmd_install = CONF.clients_chef.cmd_install.format(cookbook)
            resp_install = self.execute_command(cmd_install)
            msg = {
                'success': True,
                'response': resp_install
            }
            for line in resp_install.splitlines():
                if "ERROR" in line:
                    msg['success'] = False
        except Exception as e:
            self.disconnect_session()
            LOG.error(_LW("Chef install exception %s") % e)
            raise CookbookInstallException(cookbook=cookbook)
        return msg

    def connect_session(self):
        """
        Connect to a session with the internal parameters
        :return:
        """
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.ssh.connect(
                self._ip,
                username=self._username,
                password=self._password
            )
        except Exception as e:
            LOG.error(_LW("SSH connect exception %s") % e)
            raise SshConnectException(host=self._ip)

    def disconnect_session(self):
        """close session on exit
        """
        self.ssh.disconnect()

    def execute_command(self, command):
        """Execute a command in the given container
        :param command:  bash command to run
        :return:  execution result
        """
        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdin.flush()
        return stdout
