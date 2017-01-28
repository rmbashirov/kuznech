#!/bin/bash
set -e

REL_PATH_TO_SCRIPT=$(dirname "${BASH_SOURCE[0]}")
cd "${REL_PATH_TO_SCRIPT}"	# it's possible to run the script from some other dir, it can to "cd" on its own
NAME=$(basename "$PWD")
IMAGENAME="${NAME}"

source params.sh

CONTNAME="--name=${NAME}"

COMMAND="/bin/bash"
if [ $# -ne 0 ]
then
    COMMAND="$@"	# pass all arguments of the script
fi

nvidia-docker run --rm -ti ${OTHER_VOLUMES} ${X11_VOLUMES} ${DISPLAY} ${NET} ${CONTNAME} ${IMAGENAME} ${COMMAND}
