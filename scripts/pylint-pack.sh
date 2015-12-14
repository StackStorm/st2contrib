#!/usr/bin/env bash
# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Script which runs pylint on all the Python files in a particular pack.
#

PACK_PATH=$1
PACK_NAME=$(basename ${PACK_PATH})

PACK_REQUIREMENTS_FILE="${PACK_PATH}/requirements.txt"
PACK_TESTS_REQUIREMENTS_FILE="${PACK_PATH}/requirements-tests.txt"
PYTHON_BINARY=`which python`

SCRIPT_PATH=$(readlink -f $0)
DIRECTORY_PATH=$(dirname ${SCRIPT_PATH})

source ./scripts/common.sh

# Note: We assume this script is running inside a virtual environment into which we install the
# the pack dependencies. This way pylint can also correctly instrospect all the dependency,
if [[ ${PYTHON_BINARY} != *"virtualenv/bin/python" ]]; then
    echo "Script must run under a virtual environment which is created in the Make target"
    exit 2
fi

ST2_REPO_PATH=${ST2_REPO_PATH:-/tmp/st2}
ST2_COMPONENTS=$(find ${ST2_REPO_PATH}/* -maxdepth 1 -name "st2*" -type d)
PACK_PYTHONPATH=$(join ":" ${ST2_COMPONENTS})

echo "Running pylint on pack: ${PACK_NAME}"

if [ ! -d "${PACK_PATH}/actions" -a ! -d "${PACK_PATH}/sensors" -a ! -d "${PACK_PATH}/etc" ]; then
    echo "skipping pack without any actions and sensors"
    exit 0
fi

PYTHON_FILE_COUNT=$(find ${PACK_PATH}/* -maxdepth 1 -name "*.py" -type f | wc -l)

if [ "${PYTHON_FILE_COUNT}" == "0" ]; then
    echo "Skipping pack with no Python files"
    exit 0
fi

# Install per-pack dependencies
pip install --cache-dir ${HOME}/.pip-cache -q -r requirements-dev.txt

# Install test dependencies
pip install --cache-dir ${HOME}/.pip-cache -q -r requirements-pack-tests.txt

# Install pack dependencies
if [ -f ${PACK_REQUIREMENTS_FILE} ]; then
    pip install --cache-dir ${HOME}/.pip-cache -q -r ${PACK_REQUIREMENTS_FILE}
fi

# Install pack test dependencies (if any)
if [ -f ${PACK_TESTS_REQUIREMENTS_FILE} ]; then
    pip install --cache-dir ${HOME}/.pip-cache -q -r ${PACK_TESTS_REQUIREMENTS_FILE}
fi

export PYTHONPATH=${PACK_PYTHONPATH}:${PYTHONPATH}

#echo "PYTHONPATH=${PYTHONPATH}"
#echo "PYTHON_BINARY=${PYTHON_BINARY}"

find ${PACK_PATH}/* -name "*.py" -print0 | xargs -0 ${PYTHON_BINARY} -m pylint -E --rcfile=./.pylintrc && echo "No pylint issues found."
exit $?
