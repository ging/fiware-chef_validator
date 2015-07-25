############################################################
# Dockerfile for Chef Validator API
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER Pedro Verdugo <pmverdugo@dit.upm.es>

# Update the sources list
RUN apt-get update

################## BEGIN INSTALLATION ######################

# Install basic applications
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

# cryptography module build requirements
RUN apt-get install -y libffi-dev libssl-dev

# Get sources from github
RUN git clone https://github.com/ging/fi-ware-chef_validator /opt/fi-ware-chef_validator 

# Get pip to download and install requirements:
RUN pip install -r /opt/fi-ware-chef_validator/requirements.txt

##################### INSTALLATION END #####################

# Expose ports
EXPOSE 4042

# Set the default directory where CMD will execute
WORKDIR /opt/fi-ware-chef_validator

# Import default config
COPY chef_validator.conf etc/chef_validator/chef_validator.conf

# Export module path
ENV PYTHONPATH $PYTHONPATH:/opt/fi-ware-chef_validator/chef_validator

# Launch API listener
CMD ["python", "./bin/chef-validator-api.py", "--config-dir=./etc/chef_validator"]