#!/usr/bin/env bash

set -a
source config.env
set +a

uvicorn app:app --reload
