import os 
import string 
import jinja2
import random
from subprocess import Popen, PIPE 

## constants 
## text color constants
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
NC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def run(cmd: str, stdin: str=None, os_system: bool=False, return_stdout=True):
    'Execute a string as a blocking, exception-raising system call'
    ## verify assumptions 
    if type(cmd) != str:
        raise ValueError('`cmd` must be a string!')
    ## execute 
    print(OKCYAN+cmd+NC)
    if stdin is None: 
        ## no stdin 
        if not os_system:
            proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            exit_code = proc.wait() 
            stdout = proc.stdout.read().decode() 
            stderr = proc.stderr.read().decode() 
        else:
            exit_code = os.system(cmd)
            stdout = 'not captured'
            stderr = 'not captured'
    else:
        ## apply stdin 
        if type(stdin) not in [str, bytes]:
            raise ValueError('STDIN must be str or bytes!')
        if type(stdin) == str:
            ## convert to bytes
            stdin = stdin.encode() 
        proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE) 
        stdout, stderr = proc.communicate(stdin)
        stdout = stdout.decode() 
        stderr = stderr.decode() 
        exit_code = proc.returncode 
    if exit_code != 0:
        print(OKCYAN+'STDOUT: '+stdout+NC) 
        print(OKCYAN+'STDERR: '+stderr+NC) 
        raise OSError(exit_code)
    if return_stdout:
        return stdout 
    pass

def init_storage(root, config): 
    ## get job template 
    with open(f'{root}/src/k8s/init-storage-job.yaml', 'r') as f:
        job_template = jinja2.Template(f.read()) 
    ## get variable for template 
    with open(f'{root}/secret/acr/server', 'r') as f: 
        docker_server = f.read() 
    ## generate random id 
    rand_id = __random_str()  
    ## ai image tag from config
    cmd1 = f'cat {root}/secret/acr/server'
    acr_server = run(cmd1, return_stdout=True)
    image_name = acr_server + '/ai:' + config['image_tag']
    ## populate 
    job_yaml = job_template.render(rand_id=rand_id, \
            image_name=image_name) 
    ## apply 
    cmd1 = 'kubectl apply -f -'
    stdin = job_yaml.encode() 
    run(cmd1, stdin=stdin) 
    ## block until complete 
    cmd2 = f'kubectl wait --timeout=-1s --for=condition=complete job/init-storage-{rand_id}' 
    run(cmd2) 
    pass 

def run_horovod(root, config):
    ## get args 
    replicas = int(config['horovod_instances']) 
    interactive_debugging_mode = config['interactive_debugging_mode']
    ## get job templates 
    with open(f'{root}/src/k8s/horovod-job.yaml', 'r') as f: 
        job_template = jinja2.Template(f.read()) 
    ## get variable for template 
    with open(f'{root}/secret/acr/server', 'r') as f:
        docker_server = f.read() 
    ## generate random id 
    rand_id = __random_str() 
    ## ai image tag from config 
    cmd1 = f'cat {root}/secret/acr/server'
    acr_server = run(cmd1, return_stdout=True)
    image_name = acr_server + '/ai:' + config['image_tag']
    ## populate 
    job_yaml = job_template.render(rand_id=rand_id, \
            image_name=image_name, \
            replicas=replicas, \
            interactive_debugging_mode=interactive_debugging_mode) 
    ## apply 
    cmd1 = 'kubectl apply -f -' 
    stdin = job_yaml.encode() 
    run(cmd1, stdin=stdin) 
    job_id = f'horovod-job-{rand_id}'
    return job_id  

def update_pod_src(root, config, pod_name):
    run(f'kubectl exec -it {pod_name} -- rm -rf /app/src', os_system=True) 
    run(f'kubectl cp {root}/src {pod_name}:/app/src', os_system=True) 
    pass 

def __random_str(n_char=5): 
    letters = string.ascii_lowercase 
    return ''.join(random.choice(letters) for i in range(n_char))
