#!/usr/bin/env bash

VIRTUALENV_DIR=virtualenv

PACK_PATH=$1
PACK_NAME=$(basename ${PACK_PATH})

function join { local IFS="$1"; shift; echo "$*"; }

COMPONENTS=$(find /tmp/st2/* -maxdepth 1 -name "st2*" -type d)
PACK_PYTHONPATH=$(join ":" ${COMPONENTS})

echo "Running pylint on pack: ${PACK_NAME}"

if [ ! -d "${PACK_PATH}/actions" -a ! -d "${PACK_PATH}/sensors" -a ! -d "${PACK_PATH}/etc" ]; then
    echo "Skipping pack without any actions and sensors"
    exit 0
fi


# We create virtualenv and instasll all the pack dependencies. This way pylint can also
# correctly instrospect all the dependency references
PACK_VIRTUALENV_DIR="/tmp/venv-${PACK_NAME}"
PACK_REQUIREMENTS_FILE="${PACK_PATH}/requirements.txt"
PYTHON_BINARY=${PACK_VIRTUALENV_DIR}/bin/python

# Create virtualenv
if [ ! -d "${PACK_VIRTUALENV_DIR}" ]; then
    virtualenv --no-site-packages ${PACK_VIRTUALENV_DIR}

    # Install base dependencies
    ${PACK_VIRTUALENV_DIR}/bin/pip install -r requirements-dev.txt
fi

# Install per-pack dependencies
if [ -f "${PACK_REQUIREMENTS_FILE}" ]; then
    echo "Installing pack requirements.txt into ${PACK_VIRTUALENV_DIR}"

    # Install dependencies
    ${PACK_VIRTUALENV_DIR}/bin/pip install -r ${PACK_REQUIREMENTS_FILE}
    PYTHON_BINARY=${PACK_VIRTUALENV_DIR}/bin/python
fi

export PYTHONPATH=${PACK_PYTHONPATH}:${PYTHONPATH}

#echo "PYTHONPATH=${PYTHONPATH}"
#echo "PYTHON_BINARY=${PYTHON_BINARY}"
find ${PACK_PATH}/* -name "*.py" -print0 | xargs -0 ${PYTHON_BINARY} -m pylint -E --rcfile=./.pylintrc
