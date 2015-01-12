#!/bin/bash

SYSTEMUSER="stanley"
PUBKEY=""

create_user() {

  if [ $(id -u ${SYSTEMUSER} &> /devnull; echo $?) != 0 ]
  then
    echo "########## Creating system user: ${SYSTEMUSER} ##########"
    useradd ${SYSTEMUSER}
    mkdir -p /home/${SYSTEMUSER}/.ssh
    echo ${PUBKEY} > /home/${SYSTEMUSER}/.ssh/authorized_keys
    chmod 0700 /home/${SYSTEMUSER}/.ssh
    chmod 0600 /home/${SYSTEMUSER}/.ssh/authorized_keys
    chown -R ${SYSTEMUSER}:${SYSTEMUSER} /home/${SYSTEMUSER}
    if [ $(grep ${SYSTEMUSER} /etc/sudoers.d/* &> /dev/null; echo $?) != 0 ]
    then
      echo "${SYSTEMUSER}    ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers.d/st2
    fi
  fi
}

create_user
