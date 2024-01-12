#!/usr/bin/env bash

set -a
source config.env
set +a

python3 -m uvicorn app:app --reload
