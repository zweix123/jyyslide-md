#!/bin/bash

# TODO: Compatible with Windows operating system
jyyslice_md_path=$(dirname $(dirname $(readlink -f $0)))
export JYYSLICE_MD_PATH=$jyyslice_md_path

# unit
poetry run python unit/author.py

# TODO: other tests
