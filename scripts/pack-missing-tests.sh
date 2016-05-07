#!/bin/bash

if [ -n "${1}" ]; then
    DIR=${1}
else
    echo "Need a pack dir"
    exit 1
fi

ACTIONS=$(cd ${DIR}/actions;ls -1 *.py)
ACTION_COUNT=$(ls -1 ${DIR}/actions/*.py | wc -l)

ACTION_TESTS=$(cd ${DIR}/tests;ls -1 *.py)
if [ -d ${DIR}/tests/ ]; then
    ACTION_TEST_COUNT=$(ls -1 ${DIR}/tests/test_action_*.py | wc -l)
else
    ACTION_TEST_COUNT=0
fi

MISSING_COUNT=0

echo "Missing tests for these actions:"
for ACTION in ${ACTIONS}; do 
    if [ ! -f  ${DIR}/tests/test_action_${ACTION} ]; then 
	echo -e "\t${ACTION}"
	MISSING_COUNT=$((MISSING_COUNT+1))
    fi
done

echo 
echo "Tests with no actions:"
for TEST in ${ACTION_TESTS}; do 
    if [ ! -f ${DIR}/actions/${TEST#test_action_} ]; then
	echo -e "\t$TEST"
    fi
done

echo
echo "Total missing tests: ${MISSING_COUNT}"

echo
echo "Stats: ${ACTION_TEST_COUNT} test for ${ACTION_COUNT} actions"
