#!/bin/bash
set -e

cd /caffe

make all -j$(nproc)
make pycaffe