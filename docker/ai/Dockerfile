
## base image
FROM ubuntu 

## define spark and hadoop versions
ENV HADOOP_VERSION 2.7.3
ENV SPARK_VERSION 2.2.1

## requirements 
RUN apt-get update && \
    apt-get install -y \
        vim \
        openjdk-8-jdk \
        python3-pip && \
    pip3 install \
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
ADD common.sh spark-master spark-worker /
ADD spark-defaults.conf /opt/spark/conf/spark-defaults.conf
ENV PATH $PATH:/opt/spark/bin

## TODO Don't copy-in scripts until run-time 
# ADD example_module.py example_module.py 

