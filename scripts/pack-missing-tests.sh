#!/bin/bash

if [ -n "${1}" ]; then
    PACK=${1}
else
    echo "Need a pack "
    exit 1
fi

echo -e "====== ${PACK} ======\n"

if [ -d ${PACK}/actions ]; then
    ACTIONS=$(cd ${PACK}/actions;ls -1 *.py)
    ACTION_COUNT=$(ls -1 ${PACK}/actions/*.py | wc -l)
else
    ACTIONS=""
    ACTION_COUNT=0
fi

if [ -d ${PACK}/tests/ ]; then
    ACTION_TESTS=$(cd ${PACK}/tests;ls -1 test_action_*.py)
    ACTION_TEST_COUNT=$(ls -1 ${PACK}/tests/test_action_*.py | wc -l)
else
    ACTION_TEST_COUNT=0
    ACTION_TESTS=""
fi

MISSING_COUNT=0

echo "Actions missing tests:"
for ACTION in ${ACTIONS}; do 
    if [ ! -f  ${PACK}/tests/test_action_${ACTION} ]; then
	echo -e "\t${ACTION}"
	MISSING_COUNT=$((MISSING_COUNT+1))
    fi
done

echo 
echo "Tests with no actions:"
for TEST in ${ACTION_TESTS}; do 
    if [ ! -f ${PACK}/actions/${TEST#test_action_} ]; then
	echo -e "\t$TEST"
    fi
done

echo
echo -e "Coverage:"
echo -e "\tActions: ${ACTION_TEST_COUNT}/${ACTION_COUNT}"
