#!/bin/bash

COMMAND=$1

if [[ ! -z $2 ]]
then
  ARGS=$2
fi

$COMMAND $ARGS
