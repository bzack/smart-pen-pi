#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYENV=${DIR}/../pyenv/smart-pen-pi

python3 -m venv "${PYENV}"
source "${PYENV}/bin/activate"
pip install --upgrade pip
pip install -r "${DIR}/requirements.txt"
