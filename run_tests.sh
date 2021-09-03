#!/usr/bin/env sh
python3 -m pip install -r tests/requirements.txt
python3 -m pip install -e .
python3 -m pytest
