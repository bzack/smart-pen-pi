#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

AUTH_KEYS=${DIR}/authorized_keys.d
AUTH_KEYS_FILE=${HOME}/.ssh/authorized_keys

printf /dev/null > $AUTH_KEYS_FILE

for f in ${AUTH_KEYS}/*; do
    cat $f >> $AUTH_KEYS_FILE
    printf "\n" >> $AUTH_KEYS_FILE 
done
