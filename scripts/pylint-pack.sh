#!/usr/bin/env bash

PACK_PATH=$1
PACK_NAME=$(basename ${PACK_PATH})

function join { local IFS="$1"; shift; echo "$*"; }

COMPONENTS=$(find /tmp/st2/* -maxdepth 1 -name "st2*" -type d)
PYTHONPATH=$(join ":" ${COMPONENTS})

echo "Running pylint on pack: ${PACK_NAME}"

if [ ! -d "${PACK_PATH}/actions" -a ! -d "${PACK_PATH}/sensors" ]; then
    echo "Skipping pack without any actions and sensors"
    exit 0
fi

#echo "PYTHONPATH=${PYTHONPATH}"
export PYTHONPATH=${PYTHONPATH}
find ${PACK_PATH}/* -name "*.py" -print0 | xargs -0 pylint -E --rcfile=./.pylintrc
