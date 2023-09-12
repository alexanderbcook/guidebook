#!/usr/bin/env bash

set -a
source config.env
set +a

flask run --debug
