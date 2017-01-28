#!/bin/bash
set -e

# cuda
#CUDA_DEVICES=$(\ls /dev/nvidia* | xargs -I{} echo '--device {}:{}')
#CUDA_SO=$(\ls /usr/lib/x86_64-linux-gnu/libcuda.* | xargs -I{} echo '-v {}:{}')

X11_VOLUMES="-v /tmp/.X11-unix:/tmp/.X11-unix -v ${HOME}/.Xauthority:/root/.Xauthority"
DISPLAY="-e DISPLAY=$DISPLAY"
NET="-p 8888:8888 --net=host"

# OTHER_DEVICES=$(\ls /dev/video* | xargs -I{} echo '--device {}:{}') # webcams

#DQ_PATH="/usr/local/cuda/samples/1_Utilities/deviceQuery/deviceQuery"
#OTHER_VOLUMES="-v ${DQ_PATH}:/usr/bin/deviceQuery -v $PWD/../../caffe:/caffe -v $PWD/../../data:/root/data"

OTHER_VOLUMES="-v $PWD/../../caffe:/caffe -v $PWD/../../data:/root/data"
