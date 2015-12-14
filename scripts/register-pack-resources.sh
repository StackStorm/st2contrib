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

ST2_REPO_PATH=${ST2_REPO_PATH:-/tmp/st2}

REGISTER_SCRIPT_PATH="${ST2_REPO_PATH}/st2common/bin/st2-register-content"
REGISTER_SCRIPT_FLAGS="-v --register-fail-on-failure --config-file=${ST2_REPO_PATH}/conf/st2.tests.conf --register-all"

echo "Registering all content from pack ${PACK_NAME}"
${REGISTER_SCRIPT_PATH} ${REGISTER_SCRIPT_FLAGS} --register-pack=${PACK_PATH}
exit $?
