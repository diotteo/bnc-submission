#! /bin/sh

APP_REL_PATH=$(pwd)/$(dirname $0)/../mind_map

cd ${APP_REL_PATH}

if coverage run --source=. -m unittest tests/unittest_processing.py tests/unittest_models.py tests/unittest_nodes.py tests/unittest_processing.py tests/unittest_routes.py; then
	coverage html
	xdg-open htmlcov/index.html &
fi
