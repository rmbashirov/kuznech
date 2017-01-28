#!/bin/bash
set -e

# CUDA_DEVICES=$(\ls /dev/nvidia* | xargs -I{} echo '--device {}:{}')
# CUDA_SO=$(\ls /usr/lib/x86_64-linux-gnu/libcuda.* | xargs -I{} echo '-v {}:{}')

X11_VOLUMES="-v /tmp/.X11-unix:/tmp/.X11-unix -v ${HOME}/.Xauthority:/root/.Xauthority"
DISPLAY="-e DISPLAY=$DISPLAY"
NET="--net=host"

#DQ_PATH="/usr/local/cuda/samples/1_Utilities/deviceQuery/deviceQuery"
#OTHER_VOLUMES="-v ${DQ_PATH}:/usr/bin/deviceQuery -v $PWD/../../workdir:/workdir -w=/workdir"

OTHER_VOLUMES="-v $PWD/../../workdir:/workdir -w=/workdir"