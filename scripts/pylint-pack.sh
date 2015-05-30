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

PYTHON_FILE_COUNT=$(find ${PACK_PATH}/* -maxdepth 1 -name "*.py" -type f | wc -l)

if [ "${PYTHON_FILE_COUNT}" == "0" ]; then
    echo "Skipping pack with no Python files"
    exit 0
fi

# We create a single global virtualenv which is requires with all the packs and install all the
# pack dependencies. This way pylint can also correctly instrospect all the dependency references.
PACK_VIRTUALENV_DIR="/tmp/venv-packs"
PACK_REQUIREMENTS_FILE="${PACK_PATH}/requirements.txt"
PYTHON_BINARY=${PACK_VIRTUALENV_DIR}/bin/python

# Install per-pack dependencies
if [ -f "${PACK_REQUIREMENTS_FILE}" ]; then
    PYTHON_BINARY=${PACK_VIRTUALENV_DIR}/bin/python

    if [ ! -d "${PACK_VIRTUALENV_DIR}" ]; then
        echo "Installing pack requirements.txt into ${PACK_VIRTUALENV_DIR}"

        # Create virtualenv
        virtualenv --no-site-packages ${PACK_VIRTUALENV_DIR}
    fi

    # Install base dependencies
    ${PACK_VIRTUALENV_DIR}/bin/pip install -q -r requirements-dev.txt

    # Install pack dependencies
    ${PACK_VIRTUALENV_DIR}/bin/pip install -q -r ${PACK_REQUIREMENTS_FILE}
else
    PYTHON_BINARY=`which python`
fi

export PYTHONPATH=${PACK_PYTHONPATH}:${PYTHONPATH}

#echo "PYTHONPATH=${PYTHONPATH}"
#echo "PYTHON_BINARY=${PYTHON_BINARY}"

find ${PACK_PATH}/* -name "*.py" -print0 | xargs -0 ${PYTHON_BINARY} -m pylint -E --rcfile=./.pylintrc && echo "No pylint issues found."
exit $?
