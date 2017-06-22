#!/bin/bash -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

rm -rf ${DIR}/../database.db
cat ${DIR}/create_table.sql | sqlite3 ${DIR}/../database.db
