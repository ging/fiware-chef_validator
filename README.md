FI-Ware Chef Validator
======================
Description
-----------

An OpenStack validator for the deployment of chef recipes implemented as
a service with an OpenStack-native Rest API

Features Implemented
--------------------
A RESTful API for validation

Installation Manual
-------------------
The installation manual is provided in rst format in the folder doc/source/adminmanual.rst

Installation Verification
-------------------------
The sanity check procedures are detailed in doc/source/adminmanual.rst

User Manual
-----------
The user manual is provided in rst format in the folder doc/source/usermanual.rst

API Documentation
-----------------

The API definition can be found at <http://docs.chefvalidatorapi.apiary.io/#>

License
-------

Apache License Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

Getting Started
---------------

To run the code you can clone the git repo with:

    git clone git@github.com:ging/fi-ware-chef_validator.git

Installing Dependencies
-----------------------

To install package dependencies you must run:

    pip install -r requirements.txt

Executing the listener API
--------------------------

The listener api can be manually launched with the following command:

    chef_validator/cmd/chef-validator-api.py --config-dir etc/chef_validator


External Dependencies
---------------------

The system deployment depends on several external services for
successful completion. The dependency list reads as follows:

- **OpenStack Keystone server**: Used for issuing user tokens for several OpenStack services
- **OpenStack Glance server**: Used for listing the available virtual machine images
- **OpenStack Nova server**: Used for deploying the selected virtual machine
- **Docker Server**: Used for managing the chef server image
- **Chef server**: Used to coordinate chef activities

Validation Process
------------------

The recipe validation process consists on the following steps:

1. The **Client** sends a POST request to the service API, containing:
    - The name of the recipe to be tested
    - The *Github* repository from which to obtain the recipe
    - The virtual machine name for deployment

2. The **Server** receives the request and takes the following steps:
    - Checks the user permissions to take the next steps by validating against Keystone
    - Downloads the needed *recipe*
    - Deploys the selected *Virtual Machine* image
    - Instructs the **Chef Server** to deploy the *recipe* in the given *Virtual Machine*
    - Responds to the **Client** request informing of the status of the validation process

Example Client:
---------------
An example client is provided in cmd/chef-validator-client. It can be run with the following command:

    chef_validator/cmd/chef-validator-client.py --validator_url=${url_of_the_validator_api} --username=${username} --password=${password} --image=${author/image_name} --recipe=${recipe_name}

Chef Image generation
---------------------
A default chef-solo image can be automatically generated and uploaded to the glance server with the following command:

    chef_validator/cmd/generate_image.py --username=${username} --password=${password} --auth_url={$auth_url} --tag=${author/image_tag} --config-dir {configuration_dir}

