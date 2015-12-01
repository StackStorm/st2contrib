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

# Script which prepares the environment and runs tests for a particular pack

PACK_PATH=$1

if [ ! ${PACK_PATH} ]; then
    echo "Usage: $0 <pack path>"
    exit 2
fi

if [ ! -d ${PACK_PATH} ]; then
    echo "Invalid pack path: ${PACK_PATH}"
    exit 2
fi

SCRIPT_PATH=$(readlink -f $0)
DIRECTORY_PATH=$(dirname ${SCRIPT_PATH})

source ${DIRECTORY_PATH}/common.sh

PACK_NAME=$(basename ${PACK_PATH})
PACK_TESTS_PATH="${PACK_PATH}/tests/"

SENSORS_PATH="${PACK_PATH}/sensors/"
ACTIONS_PATH="${PACK_PATH}/actions/"

###################
# Environment setup
###################

ST2_REPO_PATH=${ST2_REPO_PATH:-/tmp/st2}
ST2_COMPONENTS=$(find ${ST2_REPO_PATH}/* -maxdepth 0 -name "st2*" -type d)

PACK_REQUIREMENTS_FILE="${PACK_PATH}/requirements.txt"
PACK_PYTHONPATH="$(join ":" ${ST2_COMPONENTS}):${SENSORS_PATH}:${ACTIONS_PATH}"

# Install st2 dependencies
pip install --cache-dir ${HOME}/.pip-cache -q -r ${ST2_REPO_PATH}/requirements.txt

# Install test dependencies
pip install --cache-dir ${HOME}/.pip-cache -q -r requirements-pack-tests.txt

# Install pack dependencies
if [ -f ${PACK_REQUIREMENTS_FILE} ]; then
    pip install --cache-dir ${HOME}/.pip-cache -q -r ${PACK_REQUIREMENTS_FILE}
fi

# Set PYTHONPATH, make sure it contains st2 components in PATH
export PYTHONPATH="${PYTHONPATH}:${PACK_PYTHONPATH}"

echo "Running tests for pack: ${PACK_NAME}"

if [ -d ${PACK_TESTS_PATH} ]; then
    nosetests -s -v ${PACK_TESTS_PATH} || exit 1
fi
