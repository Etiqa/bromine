#!/usr/bin/env bash
echo 'PYTHONPATH=src pylint src/bromine'
PYTHONPATH=src pylint src/bromine

for f in tests/*.py
do
    echo "PYTHONPATH=src pylint ${f}"
    PYTHONPATH=src pylint ${f}
done

for f in *.py
do
    echo "pylint ${f}"
    pylint ${f}
done
