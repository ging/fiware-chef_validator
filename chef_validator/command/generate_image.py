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
"""Helper tool to generate a valid chef-solo glance image in docker format"""

import logging
import gc as collector
import os
import subprocess
import sys
from docker import Client as DockerClient
from glanceclient.v2 import client as GlanceClient
from oslo_config import cfg

# If ../chef_validator/__init__.py exists, add ../ to Python search path,
# so that it will override what happens to be installed in
# /usr/(local/)lib/python...
root = os.path.abspath(
    os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir)
)
if os.path.exists(os.path.join(root, 'chef_validator', '__init__.py')):
    sys.path.insert(0, root)

if 'config_dir' not in cfg.CONF:
    cfg.CONF.config_dir = "/etc/chef_validator"

from chef_validator.common.credentials import get_glance_connection

opts = [
    cfg.StrOpt('url'),
    cfg.StrOpt('image'),
]

CONF = cfg.CONF
CONF.register_opts(opts, group="clients_docker")
LOG = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


def dock_image():
    """generate docker image"""
    import sys
    import os
    status = True
    dc = DockerClient(base_url=CONF.clients_docker.url)
    # inject config files dir to syspath
    print CONF.config_dir
    wp = os.path.abspath(CONF.config_dir)
    sys.path.insert(0, wp)
    os.chdir(wp)
    with open("ChefImage.docker") as dockerfile:
        resp = dc.build(
            fileobj=dockerfile,
            rm=True,
            tag=CONF.clients_docker.image
        )
    for l in resp:
        if "error" in l.lower():
            status = False
        LOG.debug(l)
    return status


def cmdline_upload():
    """upload docker image to glance via commandline"""
    # only admin can upload images from commandline
    os.environ.update({'OS_USERNAME': 'admin'})
    cmd = "docker save {name} | " \
          "glance image-create " \
          "--is-public=True " \
          "--container-format=docker " \
          "--disk-format=raw " \
          "--name {name}".format(name=CONF.tag)
    logging.info("Executing %s" % cmd)
    subprocess.call([cmd], shell=True)


def upload_to_glance():
    """upload docker image to glance via buffer"""
    LOG.debug("Connecting Glance Client")
    gdata = get_glance_connection()
    gc = GlanceClient.Client(**gdata)
    for im in gc.images.list():
        if CONF.tag in im.name:
            LOG.debug("Deleting old Glance Image")
            gc.images.delete(im.id)
    # FIXME Memory starvation even with intermediate file
    dump_docker_image()
    upload_glance_image_from_file(gc)
    cmdline_upload()


def dump_docker_image():
    """generate file from docker image"""
    LOG.debug("Dumping Docker Image %s" % CONF.tag)
    dc = DockerClient(base_url=CONF.clients_chef.url)
    with open("/tmp/temp.tar", 'wb') as image_tar:
        image_tar.write(dc.get_image("%s:latest" % CONF.tag).data)
    del dc
    collector.collect()


def upload_glance_image_from_file(gc):
    """upload file image to glance
    :param gc:
    """
    LOG.debug("Generating Glance Image")
    with open("/tmp/temp.tar", 'rb') as image_tar:
        gc.images.create(
            name=CONF.tag,
            is_public='true',
            container_format='docker',
            disk_format='raw',
            data=image_tar
        )
    collector.collect()


def main():
    """
    Generates a Docker Image of ChefSDK based on a local dockerfile.
    Uploads the generated image to the Glance server.
    :return:
    """
    ok = dock_image()
    if ok:
        cmdline_upload()
        # upload_to_glance()


if __name__ == '__main__':
    main()
