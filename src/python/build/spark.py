from build.util import run 

def deploy_spark(root, conf): 
    ## get configs 
    cmd1 = f'cat {root}/secret/acr/server'
    acr_server = run(cmd1, return_stdout=True)
    image_name = acr_server + '/ai:' + conf['image_tag'] 
    spark_replicas = int(conf['spark_replicas'])
    storage_key = conf['storage_key'] 
    gpu = 0
    if conf['gpu']: 
        gpu = 1
        cmd2 = f'helm upgrade spark-gpu {root}/src/helm/spark-gpu --install '+\
                f'--set image={image_name} '+\
                f'--set spark_replicas={spark_replicas} '+\
                f'--set storage_key="{storage_key}" '+\
                f'--set gpu={gpu}' 
    else: 
        cmd2 = f'helm upgrade spark {root}/src/helm/spark --install '+\
                f'--set image={image_name} '+\
                f'--set spark_replicas={spark_replicas} '+\
                f'--set storage_key="{storage_key}" ' 
        pass 
    ## deploy 
    run(cmd2, os_system=True) 
    pass 

