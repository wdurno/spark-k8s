
## base image
FROM ubuntu:20.04 

## define spark and hadoop versions
#ENV HADOOP_VERSION 2.7.3
ENV HADOOP_VERSION 3.3.1 
ENV SPARK_VERSION 3.2.1
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONPATH /work
ENV SPARK_HOME /opt/spark
ENV PATH $SPARK_HOME:$PATH 
ENV HADOOP_HOME /opt/hadoop
ENV LD_LIBRARY_PATH /opt/hadoop/lib/native

## requirements 
RUN apt-get update && \
    apt-get install -y \
        vim \
        curl \
        zip \
        unzip \
        xvfb \
        tmux \
        fluxbox \
        x11vnc \
        openjdk-8-jdk && \
    ## install python3.7, since PySpark doesn't like 3.8 
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt install python3.7 -y && \
    apt install python3.7-distutils -y && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.7 get-pip.py && \
    ## symbolic link from python to python3 
    ln -s python3.7 /bin/python && \
    rm /bin/python3 && \ 
    ln -s python3.7 /bin/python3  

RUN pip3.7 install \
        numpy \
        pandas \
        torch \
        tqdm \
        gym \
        pygame \
        azure-storage-blob \
        matplotlib \
        pyspark \
        scipy  

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
ADD src/python/debug.py /work/debug.py 
ADD src/scripts/run-worker.sh /run-worker.sh
