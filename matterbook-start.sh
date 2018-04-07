#!/bin/bash
BASE_DIR=`dirname "$(readlink -f "$0")"`
cd "$BASE_DIR"

source venv/bin/activate
nohup python ./matterbook.py >/dev/null 2>&1 &

cd "$OLDPWD"
