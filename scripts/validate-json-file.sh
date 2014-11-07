#!/usr/bin/env bash

FILE=$1

echo "Validating JSON syntax for file ${FILE}..."
python -mjson.tool ${FILE} > /dev/null
