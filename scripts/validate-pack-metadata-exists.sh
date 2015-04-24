#!/usr/bin/env bash

FILE=$1

for pack in packs/*; do
    pack=$(basename "${pack}")

    if [ ${pack} == "linux" ]; then
        continue
    fi

    if [ ! -e "packs/${pack}/pack.yaml" ]; then
        echo "Pack "${pack}" is missing pack.yaml file"
        exit 1;
    fi
done

exit 0
