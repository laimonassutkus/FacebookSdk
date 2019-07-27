#!/usr/bin/env bash

PYTHON=$1
ENVIRONMENT=$2

set -e

if [ "$ENVIRONMENT" = "dev" ]
then
    ${PYTHON} setup.py sdist
    ${PYTHON} -m pip install dist/* --install-option=--environment='dev'
elif [ "$ENVIRONMENT" = "prod" ]
then
    ${PYTHON} setup.py sdist
    ${PYTHON} -m pip install dist/* --install-option=--environment='prod'
else
    echo "Unsupported environment"
    exit 1
fi

rm -rf *.egg-info build dist
