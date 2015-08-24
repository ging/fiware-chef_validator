:: Generate messages and translation files
pybabel extract -F babel.cfg -k lazy_gettext -o chef_validator/locale/chef_validator.pot .
pybabel init -i chef_validator/locale/chef_validator.pot -d chef_validator/locale -l es