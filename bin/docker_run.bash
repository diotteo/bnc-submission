#!/bin/bash

set -x

DOCKER_IMG_REF=bnc_dioo
DOCKER_NAME=bnc_dioo
APP_REL_PATH=$(pwd)/$(dirname $0)/..

cd ${APP_REL_PATH}

if ! which docker >/dev/null >&2; then
	echo "Docker is not on the PATH (not installed?), giving up" >&2
	exit 1
fi

images=( $(docker image ls -q -f reference=${DOCKER_IMG_REF}) )
case ${#images[@]} in
0)
	echo "Building image..."
	docker build -t "${DOCKER_IMG_REF}" .
	;;
1)
	;;
*)
	echo "Multiple matches for image ${DOCKER_IMG_REF}, giving up..." >&2
	exit 1
	;;
esac

containers=( $(docker container ls -q -f name=${DOCKER_NAME}) )
case ${#containers[@]} in
0)
	docker run -dit --name "${DOCKER_NAME}" -p 9999:9999 -v $(pwd):/usr/src/app:delegated "${DOCKER_IMG_REF}" bin/run.sh
	;;
1)
	docker attach "${DOCKER_NAME}"
	;;
*)
	echo "Multiple matches for container ${DOCKER_NAME}, giving up..." >&2
	exit 1
	;;
esac
