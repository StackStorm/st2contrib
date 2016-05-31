#!/usr/bin/env bash

ACTION_TEST_FILE_NAME_GLOB="test_action_*.py"

if [ -n "${1}" ]; then
    PACK=${1}
else
    echo "Need a pack "
    exit 1
fi

if [ ! -d ${PACK} ]; then
    echo "Pack directory \"${PACK}\" not found"
    exit 1
fi

echo -e "\n====== ${PACK} ======\n"

if [ -d ${PACK}/actions ]; then
    ACTIONS=$(find ${PACK}/actions -maxdepth 1 -name "*.py" -printf "%f\n")
    ACTION_COUNT=$(echo "${ACTIONS}" | grep -v ^$ | wc -l)
else
    ACTIONS=""
    ACTION_COUNT=0
fi

if [ -d ${PACK}/tests/ ]; then
    ACTION_TESTS=$(find ${PACK}/tests -maxdepth 1 -name ${ACTION_TEST_FILE_NAME_GLOB} -printf "%f\n")
    ACTION_TEST_COUNT=$(echo "${ACTION_TESTS}" | grep -v ^$ | wc -l)
else
    ACTION_TEST_COUNT=0
    ACTION_TESTS=""
fi

MISSING_COUNT=0

echo "Python Actions missing tests:"
for ACTION in ${ACTIONS}; do
    TEST_FILE_PATH=${PACK}/tests/test_action_${ACTION}
    if [ ! -f  ${TEST_FILE_PATH} ]; then
        echo -e "\t${ACTION} (${TEST_FILE_PATH} not found)"
        MISSING_COUNT=$((MISSING_COUNT+1))
    fi
done

echo
echo "Python Tests with no actions:"
for TEST in ${ACTION_TESTS}; do
    if [ ! -f ${PACK}/actions/${TEST#test_action_} ]; then
        echo -e "\t$TEST"
    fi
done

echo
echo -e "Python Test Coverage:"
echo -e "\tActions: ${ACTION_TEST_COUNT}/${ACTION_COUNT}"
