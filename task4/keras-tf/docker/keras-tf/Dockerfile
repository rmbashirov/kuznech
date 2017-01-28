FROM nvidia/cuda:7.5-cudnn5-devel

ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH

RUN mkdir -p $CONDA_DIR && \
    echo export PATH=$CONDA_DIR/bin:'$PATH' > /etc/profile.d/conda.sh && \
    apt-get update && \
    apt-get install -y wget git libhdf5-dev g++ graphviz && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda2-4.2.12-Linux-x86_64.sh && \
    /bin/bash /Miniconda2-4.2.12-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda2-4.2.12-Linux-x86_64.sh

ENV NB_USER keras
ENV NB_UID 1000

RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    mkdir -p $CONDA_DIR && \
    chown keras $CONDA_DIR -R && \
    mkdir -p /src && \
    chown keras /src

USER keras

# Python
ARG python_version=2.7.12
ARG tensorflow_version=0.10.0-cp27-none
RUN conda install -y python=${python_version} && \
    pip install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-${tensorflow_version}-linux_x86_64.whl && \
    pip install git+git://github.com/Theano/Theano.git && \
    pip install ipdb pytest pytest-cov python-coveralls coverage==3.7.1 pytest-xdist pep8 pytest-pep8 pydot_ng && \
    conda install Pillow scikit-learn notebook pandas matplotlib nose pyyaml six h5py opencv && \
    pip install git+git://github.com/fchollet/keras.git && \
    conda clean -yt

# ADD theanorc /home/keras/.theanorc

ENV PYTHONPATH='/src/:$PYTHONPATH'

WORKDIR /src