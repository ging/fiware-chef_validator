..
      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

======================================
Installation and Administration manual
======================================

Installation
============

To run the code you can clone the git repo with:

::

    git clone git@github.com:ging/fi-ware-chef_validator.git


Installing Dependencies
-----------------------

To install package dependencies you must run:

::

    pip install -r requirements.txt


Docker Container Install
------------------------

As an alternative, if you have access to a docker server, you can pull and run the latest dev build from dockerhub with:
::

    docker pull pmverdugo/fi-ware-chef_validator:dev
    docker run pmverdugo/fi-ware-chef_validator:dev


Sanity Check Procedures
=======================

Testing
-------

Nosetests are provided via the tox tool. These tests can be executed simply by typing:
::

    tox

in the root folder

Running processes
-----------------

The only running process should be
::

    /usr/bin/python chef-validator-api.py

Network Interfaces Up and Open
------------------------------

The system only uses a TCP listener port linked on all interfaces.
By default the port number is 4042, but it can be changed via the config file.

Databases
---------

In its current state the system doesn't use a database backend.

Diagnosis Procedures
====================
The Diagnosis Procedures are the first steps that a System Administrator will take to locate the source of an error in a GE.
Once the nature of the error is identified with these tests, the system admin will very often have to resort to more concrete and specific testing to pinpoint the exact point of error and a possible solution.
Such specific testing is out of the scope of this section.

Resource availability
---------------------

The system requires a functional keystone server for authentication, with a valid and updated user list.
The system also requires an accessible docker server, or alternatively a nova server.

Remote Service Access
---------------------
The system deployment depends on several external services for successful completion.
The dependency list reads as follows:

- OpenStack Keystone server:
    Used for issuing user tokens for several OpenStack services

- OpenStack Nova server/Docker server:
    Used for deploying the selected virtual machine

- Chef server:
    Used to coordinate chef activities

Resource consumption
--------------------
The system runs as a lightweigth python process, so the typical memory usage should not surpass 10MB while running.
The cpu usage should be none while listening, and should behave as a short activy spike when attending/processing.

I/O flows
---------
    - The client connects to the system via port 4042
        - The system connects to the keystone server for authentication
            - The keystone server responds
        - The system connects to the docker server for deployment
            - The docker server responds
        - Alternatively, the system connects to the nova server for deployment
            - The nova server responds
    - The server responds

License
=======

Apache License Version 2.0 http://www.apache.org/licenses/LICENSE-2.0

