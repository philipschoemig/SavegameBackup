#!/bin/sh
cd `dirname $0`/..
. .venv/bin/activate
python savegamebackup/app.py $@
deactivate
