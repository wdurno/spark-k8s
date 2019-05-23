# spark-k8s

Run a Spark cluter in a Kubernetes cluster.

**Disclaimer:** This content is based on a tutorial. See my [references](#references).

Tested on GCP. 

**steps:**
1. build & push image 
```
./build.sh 
```
2. Initialize k8s service and deployments 
```
./deploy.sh 
```
3. get master-node ID 
```
kubectl get pods 
```
4. run `PySpark` on headnode 
```
kubectl exec <head-node-id> -it pyspark 
```
5. Test it
```
x = list('aabcsed')
x = sc.parallelize(x)
x = x.map(lambda y: (y,1))
x.reduceByKey(lambda a,b: a+b).collect()
```

# References 

1. https://testdriven.io/blog/deploying-spark-on-kubernetes/
2. https://github.com/testdrivenio/spark-kubernetes 

