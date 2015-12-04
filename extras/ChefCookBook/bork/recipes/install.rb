#
# Cookbook Name:: bork
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


INSTALL_DIR = "#{node['bork'][:install_dir]}"

include_recipe 'bork::uninstall'

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

pkg_depends = value_for_platform_family(
                  'default' => %w(git curl nano wget dialog net-tools build-essential)
)

pkg_depends.each do |pkg|
  package pkg do
    action :install
  end
end

# Git resource seems to fail on master testbed server
#
# git INSTALL_DIR do
#   repository 'https://github.com/ging/bork'
#   action :sync
#   timeout 3600
# end

directory INSTALL_DIR do
  owner 'root'
  group 'root'
  action :create
end

execute 'github_download' do
  cwd INSTALL_DIR
  user 'root'
  action :run
  command 'git clone https://github.com/ging/fiware-chef_validator.git .'
end

pip_requirements INSTALL_DIR+'/requirements.txt'

include_recipe 'bork::configure'

include_recipe 'bork::start'