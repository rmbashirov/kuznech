# coca cola logos detection
This remo does not contain train.

Solution runs in nvidia-docker.

Solution uses [SSD NN](https://arxiv.org/abs/1512.02325). Achieves 72 FPS on TITAN X.

Dataset preparation scripts are stored in `misc/dataset_preparation/`.

Train data samples are stored in `misc/train_data_samples/`.

Model trained for 5 hours on TITAN X.

Inference results are stored in `ssd/data/results/cola_test/`.

To infer model on your own data:

0) Put [models](https://yadi.sk/d/TYrLzWeqykJLX) in `ssd/caffe` folder.

1) build nvidia-docker image: in `ssd/docker/ssd-nvidia/` folder run  `./build.sh`

2) run nvidia-docker image: in `ssd/docker/ssd-nvidia/` folder run `./run.sh`

3) inside nvidia-docker image: in `/caffe` folder build caffe `./build_caffe.sh`, change paths in `ssd/caffe/examples/ssd/ssd_detect_start100.py` and from `/caffe` folder run `python examples/ssd/ssd_detect_start100.py`.








