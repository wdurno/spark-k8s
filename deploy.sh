#!/bin/bash

# get credentials 
#gcloud container clusters get-credentials standard-cluster-1 --zone us-central1-a --project gdax-dnn

kubectl create -f ./kubernetes/spark-master-deployment.yaml
kubectl create -f ./kubernetes/spark-master-service.yaml

sleep 10

kubectl create -f ./kubernetes/spark-worker-deployment.yaml

