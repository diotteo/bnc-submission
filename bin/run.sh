#!/bin/sh

APP_REL_PATH=$(pwd)/$(dirname $0)/../mind_map

cd ${APP_REL_PATH}
if ! [ -f app.db ]; then
	python3 db.py
fi

python3 mind_mapper.py
