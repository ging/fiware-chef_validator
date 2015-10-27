#
# Cookbook Name:: fiware-chef_validator
# Recipe:: install
#
# Copyright 2015, GING, ETSIT, UPM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


INSTALL_DIR = "#{node['fiware-chef_validator'][:install_dir]}"

include_recipe 'fiware-chef_validator::stop'
include_recipe 'fiware-chef_validator::uninstall'

python_runtime '2' do
  version '2.7'
  options :system, dev_package: true
end

# Checking OS compatibility for chef_validator
if node['platform'] != 'ubuntu'
  log '*** Sorry, but the chef validator requires a ubuntu OS ***'
end
return if node['platform'] != 'ubuntu'

# Update the sources list
include_recipe 'apt'

#
# execute 'apt-get update' do
#   action :run
# end

pkg_depends = value_for_platform_family(
                  'default' => %w(git curl nano wget dialog net-tools build-essential)
)

pkg_depends.each do |pkg|
  package pkg do
    action :install
  end
end

git INSTALL_DIR do
  repository 'https://github.com/ging/fi-ware-chef_validator'
  action :sync
  timeout 3600
end

pip_requirements INSTALL_DIR+'/requirements.txt'

include_recipe 'fiware-chef_validator::start'