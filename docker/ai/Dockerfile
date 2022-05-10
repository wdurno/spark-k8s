
## base image
FROM ubuntu:20.04 

## define spark and hadoop versions
ENV HADOOP_VERSION 2.7.3
ENV SPARK_VERSION 2.2.1
ENV DEBIAN_FRONTEND noninteractive

## circular dependency problem...
## strange patch... 
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 871920D1991BC93C

## requirements 
RUN apt-get update && \
    apt-get install -y \
        vim \
        curl \
        openjdk-8-jdk && \
    ## install python3.7, since PySpark doesn't like 3.8 
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt install python3.7 -y && \
    apt install python3.7-distutils -y && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.7 get-pip.py && \
    ## symbolic link from python to python3 
    ln -s python3.7 /bin/python 

RUN pip3.7 install \
        numpy \
        pandas \
        torch \
        tqdm \
        pygame 

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
## TODO add from different path 
ADD src/spark/common.sh src/spark/spark-master src/spark/spark-worker /
ADD src/spark/spark-defaults.conf /opt/spark/conf/spark-defaults.conf
ENV PATH $PATH:/opt/spark/bin

## TODO Don't copy-in scripts until run-time 
ADD src/python/example_module.py example_module.py 

