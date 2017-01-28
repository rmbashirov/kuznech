#!/bin/bash
set -e

cd /caffe
python examples/ssd/ssd_pascal_start100.py 2>&1 | tee "/caffe/torun/our.log"
