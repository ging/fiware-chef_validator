#!/usr/bin/env bash
pybabel extract -F babel.cfg -k lazy_gettext -o chef_validator/locale/chef_validator.pot .
pybabel init -i chef_validator/locale/chef_validator.pot -d translations -l es