#!/usr/bin/env bash

PACK_PATH=$1
PACK_NAME=$(basename ${PACK_PATH})

PYTHON_BINARY=`which python`

function join { local IFS="$1"; shift; echo "$*"; }

echo $PYTHON_BINARY

if [[ ${PYTHON_BINARY} != *"virtualenv/bin/python" ]]; then
    echo "Script must run under a virtual environment which is created in the Make target"
    exit 2
fi

COMPONENTS=$(find /tmp/st2/* -maxdepth 1 -name "st2*" -type d)
PACK_PYTHONPATH=$(join ":" ${COMPONENTS})

echo "Running pylint on pack: ${PACK_NAME}"

if [ ! -d "${PACK_PATH}/actions" -a ! -d "${PACK_PATH}/sensors" -a ! -d "${PACK_PATH}/etc" ]; then
    echo "Skipping pack without any actions and sensors"
    exit 0
fi

PYTHON_FILE_COUNT=$(find ${PACK_PATH}/* -maxdepth 1 -name "*.py" -type f | wc -l)

if [ "${PYTHON_FILE_COUNT}" == "0" ]; then
    echo "Skipping pack with no Python files"
    exit 0
fi

# Note: We assume this script is running inside a virtual environment into which we install the
# the pack dependencies.This way pylint can also correctly instrospect all the dependency
# references.
PACK_VIRTUALENV_DIR="/tmp/venv-packs"
PACK_REQUIREMENTS_FILE="${PACK_PATH}/requirements.txt"
PYTHON_BINARY=${PACK_VIRTUALENV_DIR}/bin/python

# Install per-pack dependencies
# Install base dependencies
${PACK_VIRTUALENV_DIR}/bin/pip install -q -r requirements-dev.txt --cache-dir ${HOME}/.pip-cache

# Install pack dependencies
${PACK_VIRTUALENV_DIR}/bin/pip install -q -r ${PACK_REQUIREMENTS_FILE} --cache-dir ${HOME}/.pip-cache

export PYTHONPATH=${PACK_PYTHONPATH}:${PYTHONPATH}

#echo "PYTHONPATH=${PYTHONPATH}"
#echo "PYTHON_BINARY=${PYTHON_BINARY}"

find ${PACK_PATH}/* -name "*.py" -print0 | xargs -0 ${PYTHON_BINARY} -m pylint -E --rcfile=./.pylintrc && echo "No pylint issues found."
exit $?
