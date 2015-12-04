#!/usr/bin/env bash
cd chef_validator
python command/generate_image.py --image=pmverdugo/trusty-chef_solo:dev
cd ..
