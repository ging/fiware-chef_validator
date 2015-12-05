#!/usr/bin/env bash

# install docker
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > /etc/apt/sources.list.d/docker.list

# install docker-compose
curl -L https://github.com/docker/compose/releases/download/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# setup environment
cd test_deploy
docker-compose up &
cd ..

# server
python ../../command/chef-validator-api.py

# passed
python chef_validator_client_test.py --username=demo --password=demo --validator_url=http://127.0.0.1:4042/validate --cookbook=git --image=pmverdugo/trusty-chefdk-validate

# error
python chef_validator_client_test.py --username=demo --password=demo --validator_url=http://127.0.0.1:4042/validate --cookbook=myfakecookbook
