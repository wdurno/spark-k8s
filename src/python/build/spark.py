from build.util import run 

def deploy_spark(root, conf): 
    ## get configs 
    cmd1 = f'cat {root}/secret/acr/server'
    acr_server = run(cmd1, return_stdout=True)
    image_name = acr_server + '/ai:' + conf['image_tag'] 
    spark_replicas = int(conf['spark_replicas'])
    ## deploy 
    cmd2 = f'helm upgrade spark {root}/src/helm/spark --install '+\
            f'--set image={image_name} '+\
            f'--set spark_replicas={spark_replicas}'
    run(cmd2, os_system=True) 
    pass 

