#!/usr/bin/env bash

if [ -z ${TASK} ]; then
  echo "No task provided"
  exit 2
  fi


if [ ${TASK} == "flake8" ]; then
  make flake8
elif [ ${TASK} == "pylint" ]; then
  make pylint
elif [ ${TASK} == "configs-check" ]; then
  make configs-check
elif [ ${TASK} == "metadata-check" ]; then
  make metadata-check
elif [ ${TASK} == "packs-tests" ]; then
  make packs-tests
else
  echo "Invalid task: ${TASK}"
  exit 2
fi

exit $?
