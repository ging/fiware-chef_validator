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

import logging
import gc as collector
import os
import subprocess
from docker import Client as DockerClient
from glanceclient.v2 import client as GlanceClient
from oslo_config import cfg
from credentials import get_glance_connection

CONF = cfg.CONF
LOG = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


def dock_image():
    dc = DockerClient(base_url='unix://var/run/docker.sock')
    with open(r"./ChefImage.docker") as dockerfile:
        resp = dc.build(
            fileobj=dockerfile,
            rm=True,
            tag=CONF.tag
        )
    for l in resp:
        print l


def cmdline_upload():
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
    LOG.debug("Connecting Glance Client")
    gdata = get_glance_connection()
    gc = GlanceClient.Client(**gdata)
    for im in gc.images.list():
        if CONF.tag in im.name:
            LOG.debug("Deleting old Glance Image")
            gc.images.delete(im.id)
    # Memory starvation even with intermediate file
    # dump_docker_image()
    # upload_glance_image_from_file(gc)
    cmdline_upload()


def dump_docker_image():
    LOG.debug("Dumping Docker Image %s" % CONF.tag)
    dc = DockerClient(base_url='unix://var/run/docker.sock')
    with open("/tmp/temp.tar", 'wb') as image_tar:
        image_tar.write(dc.get_image("%s:latest" % CONF.tag).data)
    del dc
    collector.collect()


def upload_glance_image_from_file(gc):
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
    dock_image()
    upload_to_glance()

if __name__ == '__main__':
    main()
