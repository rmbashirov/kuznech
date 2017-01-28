#!/bin/bash
set -e

REL_PATH_TO_SCRIPT=$(dirname "${BASH_SOURCE[0]}")
cd "${REL_PATH_TO_SCRIPT}"	# it's possible to run the script from some other dir, it can to "cd" on its own
NAME=$(basename "$PWD")
IMAGENAME="${NAME}"

COMMAND="/bin/bash"
if [ $# -ne 0 ]
then
    COMMAND="$@"	# pass all arguments of the script
fi

nvidia-docker exec -ti ${NAME} ${COMMAND}
