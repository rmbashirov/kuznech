FROM nvidia/cuda:7.5-cudnn5-devel-ubuntu14.04

################################################################
# Anaconda
################################################################

ENV ANACONDA /root/anaconda
ENV PATH $ANACONDA/bin:$PATH
ENV LD_LIBRARY_PATH /lib/x86_64-linux-gnu:$ANACONDA/lib:$LD_LIBRARY_PATH
# ENV LD_LIBRARY_PATH $ANACONDA/lib:/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH # not working. wtf? 

# Download anaconda and install it
RUN apt-get update && apt-get install -y wget build-essential
RUN wget http://repo.continuum.io/archive/Anaconda2-4.0.0-Linux-x86_64.sh -P /tmp
RUN bash /tmp/Anaconda2-4.0.0-Linux-x86_64.sh -b -p $ANACONDA
RUN rm /tmp/Anaconda2-4.0.0-Linux-x86_64.sh
RUN conda install -y opencv

# Copy the config file into docker
RUN jupyter notebook --generate-config && ipython profile create

################################################################
# Caffe preinstall
################################################################

# Install dependencies
RUN apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    wget \
    nano \
    libprotobuf-dev \
    libopencv-dev \
    libhdf5-serial-dev \
    protobuf-compiler \
    libhdf5-serial-dev \
    libboost-all-dev \
    libatlas-base-dev \
    libleveldb-dev \
    libsnappy-dev \
    libgflags-dev \
    libgoogle-glog-dev \
    liblmdb-dev \
    libtiff4-dev

RUN cd /usr/lib/x86_64-linux-gnu && \
    ln -s libhdf5.so.7 libhdf5.so.10 && \
    ln -s libhdf5_hl.so.7 libhdf5_hl.so.10 && \
    ln /dev/null /dev/raw1394 && \
    ldconfig

# Set environment variables
ENV PYTHONPATH /caffe/python:$PYTHONPATH


# Add Python support
COPY "build_files/requirements.txt" "/tmp/requirements.txt"
WORKDIR /tmp
RUN for req in $(cat requirements.txt); do pip install $req; done

WORKDIR /caffe