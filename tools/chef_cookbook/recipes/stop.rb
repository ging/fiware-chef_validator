#
# Cookbook Name:: 
# Recipe:: 
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

bash 'stop chef_validator' do
  user 'root'
  ignore_failure true
  code <<-EOH
    pkill -f "python /opt/fiware-chef_validator/chef_validator/cmd/chef-validator-api.py --config-dir=etc/chef_validator"
  EOH
end