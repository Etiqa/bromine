#!/usr/bin/env bash

set -x

PYTHONPATH=src pylint src/bromine

PYTHONPATH=src pylint tests

for f in *.py; do
    pylint "${f}"
done
