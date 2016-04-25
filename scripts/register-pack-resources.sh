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
# Script which tries to register all the resources from a particular pack and
# fails (exits with non-zero) if registering a particular resource fails.
#

PACK_PATH=$1
PACK_NAME=$(basename ${PACK_PATH})

source ./scripts/common.sh

ST2_REPO_PATH=${ST2_REPO_PATH:-/tmp/st2}
ST2_COMPONENTS=$(get_st2_components)
PACK_PYTHONPATH=$(join ":" ${ST2_COMPONENTS})

REGISTER_SCRIPT_PATH="${ST2_REPO_PATH}/st2common/bin/st2-register-content"
# Note: -v verbose flag has been removed to work around Travis log size limits
REGISTER_SCRIPT_COMMON_FLAGS="--register-fail-on-failure --config-file=scripts/st2.tests.conf"

# Note: Rules in some packs rely on triggers which are created lazily later on
# so we can't test rule registration for those packs.
if [ ${PACK_NAME} = "sensu" ] || [ ${PACK_NAME} = "nagios" ]  || [ ${PACK_NAME} = "hubot" ]; then
    REGISTER_SCRIPT_REGISTER_FLAGS="--register-sensors --register-actions --register-aliases --register-policies"
else
    REGISTER_SCRIPT_REGISTER_FLAGS="--register-all"
fi

# Install st2 dependencies
pip install --cache-dir ${HOME}/.pip-cache -q -r ${ST2_REPO_PATH}/requirements.txt

# Set PYTHONPATH to include st2 components
export PYTHONPATH=${PACK_PYTHONPATH}:${PYTHONPATH}

echo "Registering content from pack ${PACK_NAME}"
${REGISTER_SCRIPT_PATH} ${REGISTER_SCRIPT_COMMON_FLAGS} ${REGISTER_SCRIPT_REGISTER_FLAGS} --register-pack=${PACK_PATH}
EXIT_CODE=$?

if [ ${EXIT_CODE} -ne 0 ]; then
    echo "Registering resources for pack ${PACK_NAME} failed"
fi

exit ${EXIT_CODE}
