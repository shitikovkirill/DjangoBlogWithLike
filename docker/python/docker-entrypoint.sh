#!/bin/bash

if [[ "$DEBUG" = "true" ]]
then
    set -x
    TOX_OPTIONS=$TOX_OPTIONS" -vvvv "
fi

tox -e devenv $TOX_OPTIONS

source /app/venv/bin/activate

exec "$@"
