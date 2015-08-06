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

from docker import Client


def main():
    cli = Client(base_url='unix://var/run/docker.sock')
    with open(r"./ChefImage.docker") as dockerfile:
        resp = cli.build(
            fileobj=dockerfile,
            rm=True,
            tag="pmverdugo/chef-standalone"
        )
    for l in resp:
        print l

if __name__ == '__main__':
    main()
