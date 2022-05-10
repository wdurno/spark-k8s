# spark-k8s

Run a Spark cluter in a Kubernetes cluster. Execute custom module imported from worker nodes. 

This content is based on a tutorial. See my [references](#references).

Tested on GCP. 

**steps:**
1. Copy `spark-k8s-config.yaml` to your home directory and configure.
2. Deploy infrastructure with Terraform. Build your Spark base image. Deploy a Spark cluster.
```
python3 cli.py 
```
4. run `PySpark` on headnode 
```
kubectl exec -it spark-master-0 -- pyspark 
```
5. Test it
```
from example_module import func 
x = sc.parallelize(range(100),20)
y = x.map(str) 
z = y.map(func)
z.collect()
```

