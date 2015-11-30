#!/usr/bin/env bash

# passed
python chef-validator-client_test.py --username=demo --password=demo --validator_url=http://127.0.0.1:4042 --cookbook=git
# error
python chef-validator-client_test.py --username=demo --password=demo --validator_url=http://127.0.0.1:4042 --cookbook=myfakecookbook