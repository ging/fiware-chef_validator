# coding=utf-8

FI-Ware Chef Validator
======================

An OpenStack validator for the deployment of chef cookbooks implemented as
a service with an OpenStack-native REST API

Getting Started
---------------

To run the code you can clone the git repo with:

::

    git clone git@github.com:ging/fi-ware-chef_validator.git

Installing Dependencies
-----------------------

To install package dependencies you must run:

::

    pip install -r requirements.txt

API Definition
--------------

The API definition can be found at http://docs.chefvalidatorapi.apiary.io/#

External Dependencies
---------------------

The system deployment depends on several external services for successful task completion.
The dependency list reads as follows:

- OpenStack Keystone server:
    Used for issuing user tokens for several OpenStack services

- OpenStack Glance server:
    Used for listing the available virtual machine images

- OpenStack Nova server:
    Used for deploying the selected virtual machine

Validation Process
------------------

The cookbook validation process consists on the following steps:

1. The **Client** sends a POST request to the service API, containing:
    - The name of the cookbook to be tested
    - The *chef supermarket* repository from which to obtain the cookbook
    - The virtual machine name for deployment
2. The **Server** receives the request and takes the following steps:
    - Checks the user permissions to take the next steps by validating against Keystone
    - Downloads the needed *cookbook*
    - Deploys the selected *Virtual Machine* image
    - Instructs the **Chef Server** to deploy the *cookbook* in the given *Virtual Machine*
    - Responds to the **Client** request informing of the status of the validation process

License
-------

Apache License Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
