#!/usr/bin/env sh
python -m pip install -r tests/requirements.txt
python -m pip install -e .
python -m pytest
