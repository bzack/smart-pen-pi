#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PKG_FILE=$DIR/setup/packages.txt

sudo apt-get install -y $(grep -vE "^\s*#" "${PKG_FILE}"  | tr "\n" " ")
