#!/usr/bin/env bash

FILE=$1

echo "Validating YAML syntax for file ${FILE}..."
python -c "import yaml; yaml.safe_load(open('${FILE}', 'r'))"
exit $?
