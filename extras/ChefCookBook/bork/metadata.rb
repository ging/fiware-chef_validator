name              'bork'
maintainer        'GING-DIT-ETSIT-UPM'
maintainer_email  'ging@dit.upm.es'
description       'A cookbook for deploying the bork component'
version           '0.0.1'
long_description  IO.read(File.join(File.dirname(__FILE__), 'README.md'))

depends           'build-essential'
depends           'poise-python'
depends           'git'
depends           'apt'

%w{ ubuntu }.each do |os|
  supports os
end