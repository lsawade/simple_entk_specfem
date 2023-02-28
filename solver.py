import toml
from radical.entk import Pipeline, Stage, Task, AppManager
import traceback, sys, os

# Load config
cfg = toml.load('entk.toml')

# Set radical environment flags
for key, value in cfg['radical']['env'].items():
    os.environ[key] = str(value)

# Setup rabbitmq
rmq = cfg['RMQ']
hostname = rmq['HOSTNAME']
port = rmq['PORT']
password = rmq['PASSWORD']
username = rmq['USERNAME']

# Set environment URL
os.environ["RADICAL_PILOT_DBURL"] = f"mongodb://{username}:{password}@{hostname}/specfm"

# Print setup
print("Setup:\n--------")
print(hostname)
print(port)
print(password[:2] + "*" * (len(password)-4) + password[-2:])
print(username)

specfem = "/gpfs/alpine/geo111/world-shared/lsawade/specfem3d_globe"



if __name__ == '__main__':
    p = Pipeline()

    # Hello World########################################################
    test_stage = Stage()
    test_stage.name = "HelloWorldStage"

    # Create 'Hello world' task
    t = Task()
    t.pre_exec = [
        '. /sw/summit/lmod/lmod/init/profile',
        'module load spectrum-mpi gcc']
    t.name = "HelloWorldTask"
    t.executable = '/bin/echo'
    t.arguments = ['"Hello world"']
    t.stdout = 'STDOUT'
    t.stderr = 'STDERR'
    t.download_output_data = ['STDOUT', 'STDERR']

    # Add task to stage and stage to pipeline
    test_stage.add_tasks(t)
    p.add_stages(test_stage)
       
    specfem_stage = Stage()
    specfem_stage.name = 'SimulationStage'
    
    for i in range(2):

        # Create Task
        t = Task()
        t.name = f"SIMULATION.{i:0>2d}"
        tdir = f"/gpfs/alpine/geo111/world-shared/lsawade/entk_test/specfem_run_{i+1}"
        # t.sandbox = tdir
        t.pre_exec = [
            '. /sw/summit/lmod/lmod/init/profile',
            # Load necessary modules
            'module purge',
            'module load gcc spectrum-mpi cuda cmake boost',
            f'cd {tdir}'
        ]
        t.executable = './bin/xspecfem3D'
        t.cpu_reqs = {'cpu_processes': 24, 'cpu_process_type': 'MPI', 'cpu_threads': 1, 'cpu_thread_type' : 'OpenMP'}
        t.gpu_reqs = {'gpu_processes': 1,  'gpu_process_type': None,  'gpu_threads': 1, 'gpu_thread_type' : 'CUDA'}
        t.stdout = 'STDOUT'
        t.stderr = 'STDERR'
        t.download_output_data = ['STDOUT', 'STDERR']

        # Add task to stage
        specfem_stage.add_tasks(t)
        
    p.add_stages(specfem_stage)
        
    res_dict = {
        'resource': 'ornl.summit_prte', # 'local.localhost',
        'schema' : 'local',
        'walltime':  20, #2 * 30,
        'cpus': 48,
        'gpus': 48,
        'project': 'GEO111'
    }

    appman = AppManager(hostname=hostname, port=port, username=username, password=password, resubmit_failed=False)
    appman.resource_desc = res_dict
    appman.workflow = set([p])
    appman.run()        
    
