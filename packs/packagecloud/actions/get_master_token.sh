#! /bin/bash

ORG=${1}
REPO=${2}
TOKEN_NAME=${3}

output=$(package_cloud master_token list ${ORG}/${REPO} | grep ${TOKEN_NAME} | awk '{print $2}' |  tr -d '(|)')

if [ -z ${output} ]; then
    echo "No master token found!"
    exit 1
fi

echo $output
exit 0
