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
6. Run more-complex software by recursively copying-in directory trees to each Spark pods' `/work` directory.
```
python3 cli.py --update-work-dir [dir to copy]
```
7. spark-submit
```
spark-submit \
  --master spark://spark-master:7077 \
  --supervise \
  --py-files work/regmem.py,work/az_blob_util.py,work/regmem_cnn.py,work/lanczos.py,work/nlp.py,work/miner.py \
  --files work/shakespeare_tokens.pkl \
  --conf "spark.python.worker.memory=3g" \
  work/spark-k8s-experiment-14-online-learning.py 1> stdout 2> stderr
```
