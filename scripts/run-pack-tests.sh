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

# Script which runs tests for a particular pack

PACK_PATH=$1

if [ ! ${PACK_PATH} ]; then
    echo "Usage: $0 <pack path>"
    exit 2
fi

if [ ! -d ${PACK_PATH} ]; then
    echo "Invalid pack path: ${PACK_PATH}"
    exit 2
fi

PACK_NAME=$(basename ${PACK_PATH})
PACK_TESTS_PATH="${PACK_PATH}/tests/"

echo "Running tests for pack: ${PACK_NAME}"

if [ -d ${PACK_TESTS_PATH} ]; then
    nosetests -s -v ${PACK_TESTS_PATH} || exit 1
fi
