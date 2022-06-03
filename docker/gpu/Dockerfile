FROM nvidia/cuda:11.4.0-base-ubuntu20.04

ENV HADOOP_VERSION=2.7.3 \
    SPARK_VERSION=3.2.1 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=/app/src/python:/usr/lib/python3/dist-packages \
    CONDA_AUTO_UPDATE_CONDA=false \
    PATH=/root/miniconda/bin:$PATH 


# Set default shell to /bin/bash
SHELL ["/bin/bash", "-cu"]

RUN echo "installing cudnn via miniconda..." && \
    apt-get update && apt-get install -y \
        curl \
        ca-certificates \
        sudo \
        git \
        bzip2 \
        libx11-6 && \
    rm -rf /var/lib/apt/lists/* && \
    curl -sLo ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-py38_4.8.3-Linux-x86_64.sh && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p ~/miniconda && \
    rm ~/miniconda.sh && \
    conda install -y python==3.8.3 && \
    conda clean -ya && \
    echo "CUDA 11.1-specific steps..." && \
    conda install -y -c conda-forge cudatoolkit=11.1.1 && \
    conda install -y -c pytorch \
        "pytorch=1.8.1=py3.8_cuda11.1_cudnn8.0.5_0" \
        "torchvision=0.9.1=py38_cu111" && \
    conda clean -ya

RUN echo "installing libraries..." && \
    apt-get update && apt-get install -y --allow-downgrades --allow-change-held-packages --no-install-recommends \
        build-essential \
        cmake \
        g++ \
        vim \
        wget \
        ca-certificates \
        libjpeg-dev \
        libpng-dev \
        librdmacm1 \
        libibverbs1 \
        ibverbs-providers \
        openjdk-8-jdk \
        tmux \
        xvfb \
        x11-xserver-utils \
        fluxbox \
        x11vnc \
	python3-dev \
        python3-psycopg2 \
	software-properties-common \
        freeglut3-dev 

RUN echo "installing openmpi and fundamental packages..." && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install \
        scikit-build \
        future \
        typing \
        numpy \
        scipy \
        matplotlib \
        gym \
        minerl \
        minio \
        Jinja2 \
        cassandra-driver \
        pandas \
        tqdm \
        pygame \
        pyglet \
        azure-storage-blob  

## download and install hadoop
RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | \
        tar -zx hadoop-${HADOOP_VERSION}/lib/native && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    echo Hadoop ${HADOOP_VERSION} native libraries installed in /opt/hadoop/lib/native

## download and install spark
RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz | \
        tar -zx && \
    ln -s spark-${SPARK_VERSION}-bin-hadoop2.7 spark && \
    echo Spark ${SPARK_VERSION} installed in /opt

## add scripts and update spark default config
ADD src/spark/common.sh src/spark/spark-master src/spark/spark-worker /
ADD src/spark/spark-defaults.conf /opt/spark/conf/spark-defaults.conf
ENV PATH $PATH:/opt/spark/bin

## example script 
ADD src/python/example_module.py /work/example_module.py 
ADD src/scripts/run-worker.sh /run-worker.sh 
