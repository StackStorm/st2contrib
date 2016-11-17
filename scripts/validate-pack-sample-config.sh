#!/usr/bin/env bash


if [ $# -ne 1 ]; then
    echo "Usage: ${0} <path to pack directory>"
    exit 1
fi

if [ ! -d ${PACK_DIR} ]; then
    echo "Pack directory \"${PACK_DIR}\" doesn't exist"
    exit 2
fi

PACK_DIR=$1
PACK_NAME=$(basename $PACK_DIR)

CONFIG_SCHEMA_FILE=$(find ${PACK_DIR}/config.schema.yaml)
EXAMPLE_CONFIG_FILE=$(find ${PACK_DIR}/*.yaml.example)

if [ -z ${CONFIG_SCHEMA_FILE} ]; then
    echo "Pack ${PACK_NAME} doesn't contain config.schema.yaml file"
    exit 0
fi

if [ -z ${EXAMPLE_CONFIG_FILE} ]; then
    echo "No sample config file found for pack ${PACK_NAME}"
    exit 0
else
    echo "Validating example config ${EXAMPLE_CONFIG_FILE} for pack ${PACK_NAME}..."
    /tmp/st2/st2common/bin/st2-validate-pack-config --schema-path ${CONFIG_SCHEMA_FILE} --config-path ${EXAMPLE_CONFIG_FILE}
    exit $?
fi
