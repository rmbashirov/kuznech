# Deep Dream inside nvidia-docker demo

1) Build nvidia-docker image:
```
cd keras-tf/docker/keras-tf
./build.sh
```
2) Run and enter nvidia-docker container:
```
./run.sh
```
3) You will be in nvidia-docker container in `/workdir` folder. Run deep dream:
```
./run_deep_dream.sh
```
4) Result images will be in `images` folder
