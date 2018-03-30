#!/usr/bin/env bash

set -x

PYTHONPATH=src pylint src/bromine

PYTHONPATH=src pylint tests --disable=missing-docstring

for f in *.py; do
    pylint "${f}"
done
