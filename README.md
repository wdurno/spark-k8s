# spark-k8s

Run a Spark cluter in a Kubernetes cluster. Execute custom module imported from worker nodes. 

This content is based on a tutorial. See my [references](#references).

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
kubectl exec -it <head-node-id>  pyspark 
```
5. Test it
```
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf('string')
def my_udf(x):
    import sys
    sys.path.append('/')
    from example_module import func
    return func(x)

x = list('aabcsed')
x = spark.createDataFrame(x, StringType()) 
x.select(my_udf('value')).show()  
```

If you don't believe it's running in parallel or that it must bring `example_module.py`, delete `example_module.py` from master before running the script above. It executes equivalently. 

# References 

1. https://testdriven.io/blog/deploying-spark-on-kubernetes/
2. https://github.com/testdrivenio/spark-kubernetes 

