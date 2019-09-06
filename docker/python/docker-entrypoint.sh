#!/bin/bash

if [[ "$DEBUG" = "true" ]]
then
    set -ex
fi

exec "$@"
