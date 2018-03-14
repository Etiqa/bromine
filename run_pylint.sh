#!/usr/bin/env bash

function _run_pylint() {
    _cmd=$1
    echo ${_cmd}
    eval ${_cmd}
}

_run_pylint 'PYTHONPATH=src pylint src/bromine'

_run_pylint 'PYTHONPATH=src pylint tests'

for f in *.py; do _run_pylint "pylint ${f}"; done
