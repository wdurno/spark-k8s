import os 
import sys 
import yaml 
import argparse 
from kubernetes import client, config

## args 
parser = argparse.ArgumentParser(description='Distributed fitting for RL models.') 
parser.add_argument('--config-path', dest='config_path', type=str, default=None, help='path to config file') 
parser.add_argument('--no-docker-build', dest='no_docker_build', action='store_true', help='skip docker build step') 
parser.add_argument('--keep-docker-build-env', dest='keep_docker_build_env', action='store_true', default=False, \
        help='do not tear-down DinD after build, thereby retaining cached layers') 
parser.add_argument('--terraform-destroy', dest='terraform_destroy', action='store_true', help='tears-down everything') 
parser.add_argument('--terraform-destroy-compute', dest='terraform_destroy_compute', action='store_true', \
        help='destroys nodes, retains resource group and acr') 
parser.add_argument('--skip-terraform', dest='skip_terraform', action='store_true', help='skips all terraform build actions') 
parser.add_argument('--update-work-dir', dest='update_work_dir', type=str, default=None, \
        help='clear working directory, and copy-in content for all pods') 
parser.add_argument('--update-pod-src', dest='update_pod_src', type=str, default=None, \
        help='a debugging tool. Updates a specific pod with latest src. Just an update, no Terraform nor Docker '+\
        'commands. Provide the pod name.') 
parser.add_argument('--interactive-debugging-mode', dest='interactive_debugging_mode', action='store_true', \
        help='sleeps horovod pods for easier debugging') 
parser.add_argument('--do-not-helm-install', dest='do_not_helm_install', action='store_true', \
        help='does not install horovod workers, nor sets up storage') 
parser.add_argument('--viewer-set-interactive-mode', dest='viewer_set_interactive_mode', action='store_true', \
        help='redeploy viewer in interactive mode. Take no further action.') 
parser.add_argument('--viewer-set-non-interactive-mode', dest='viewer_set_non_interactive_mode', action='store_true', \
        help='redeploy viewer in non-interactive-mode. Take no further action.') 
parser.add_argument('--do-not-run-horovod', dest='do_not_run_horovod', action='store_true', \
        help='allows for setup without running') 
args = parser.parse_args() 

## constants 
args.HOME = os.environ['HOME']  
args.ROOT = os.getcwd() 

## configure build env 
sys.path.append(os.path.join(args.ROOT, 'src', 'python')) 

## import build libs 
from build.terraform import guarantee_phase_1_architecture, guarantee_phase_2_architecture, terraform_destroy, \
        terraform_destroy_compute
from build.secret import refresh_keys 
from build.docker import docker_build
from build.spark import deploy_spark
from build.util import run 
#from build.horovod import deploy_horovod, update_horovod_worker_src 
#from build.cassandra import cassandra_deploy
#from build.minio import minio_deploy 
#from build.postgres import postgres_deploy 
#from build.viewer import viewer_deploy 
#from build.util import init_storage, run_horovod, update_pod_src 

## parse config path 
if args.config_path is None: 
    ## setting to default 
    config_path = os.path.join(args.HOME, 'spark-k8s-config.yaml') 
    pass

## load config 
with open(config_path, 'r') as f: 
    args.config = yaml.safe_load(f) 
    args.config['interactive_debugging_mode'] = args.interactive_debugging_mode 
    pass

if args.update_work_dir:
    config.load_kube_config() 
    v1 = client.CoreV1Api() 
    pod_list = v1.list_namespaced_pod('default') 
    pod_list = [pod.metadata.name for pod in pod_list.items] 
    print('clearing pods...') 
    for pod in pod_list: 
        cmd1 = f'kubectl exec -it {pod} -- rm -rf /work' 
        cmd2 = f'kubectl exec -it {pod} -- mkdir /work'
        run(cmd1, os_system=True) 
        #run(cmd2, os_system=True) 
    print('copying...') 
    for pod in pod_list: 
        cmd3 = f'kubectl cp {args.update_work_dir} {pod}:/work' 
        run(cmd3, os_system=True) 
    exit(0) 
    pass 

if args.update_pod_src:
    update_pod_src(args.ROOT, args.config, args.update_pod_src)
    exit(0) 
    pass 

if args.terraform_destroy_compute:
    terraform_destroy_compute(args.ROOT, args.config) 
    exit(0) ## TODO need arg-checking logic. Will not terraform_destroy after this point. 
    pass 

if args.terraform_destroy: 
    terraform_destroy(args.ROOT, args.config) 
    exit(0) 
    pass

if args.viewer_set_interactive_mode: 
    viewer_deploy(args.ROOT, args.config, interactive_mode=True) 
    exit(0) 
    pass 

if args.viewer_set_non_interactive_mode:
    viewer_deploy(args.ROOT, args.config, interactive_mode=False) 
    exit(0) 
    pass 

if not args.skip_terraform:
    ## deploy build-essential infrastructure 
    guarantee_phase_1_architecture(args.ROOT, args.config) 
    pass

## always refresh keys because tokens expire 
refresh_keys(args.ROOT, args.config) 

if not args.no_docker_build: 
    ## build horovod image 
    docker_build(args.ROOT, args.config, args.keep_docker_build_env) 
    pass

if not args.skip_terraform:
    ## deploy horovod compute infrastructure 
    guarantee_phase_2_architecture(args.ROOT, args.config) 
    pass 

if not args.do_not_helm_install:
    ## deploy all infrastructure 
    deploy_spark(args.ROOT, args.config) 
    pass 
#    deploy_horovod(args.ROOT, args.config)
#    cassandra_deploy(args.ROOT, args.config) 
#    minio_deploy(args.ROOT, args.config) 
#    postgres_deploy(args.ROOT, args.config) 
#    init_storage(args.ROOT, args.config) 
#    viewer_deploy(args.ROOT, args.config) 
#    pass 
#
#if not args.do_not_run_horovod: 
#    job_id = run_horovod(args.ROOT, args.config) 
#    print(f'horovod job id: {job_id}') 
#    pass 
