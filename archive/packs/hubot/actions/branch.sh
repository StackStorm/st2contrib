#!/usr/bin/env bash

BRANCH=$(cat .branch)
REF=$(cat .git/HEAD)

echo "Hubot is currently on branch ${BRANCH}, ${REF}"

