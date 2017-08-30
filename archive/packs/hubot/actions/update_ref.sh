#!/usr/bin/env bash

BRANCH=$1

echo 'ssh -i ../.ssh/id_rsa -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no $*' > ssh
chmod +x ssh
export GIT_SSH="./ssh"

git fetch -q origin && git checkout -q origin/${BRANCH} && echo $BRANCH > .branch
