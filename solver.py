from radical.entk import Pipeline, Stage, Task, AppManager
import traceback, sys, os


hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = int(os.environ.get('RMQ_PORT', 5672))
password = os.environ.get('RMQ_PASSWORD', None)
username = os.environ.get('RMQ_USERNAME', None)

print("Setup:\n--------")
print(hostname)
print(port)
print(password[:2] + "*" * (len(password)-4) + password[-2:])
print(username)

specfem = "/scratch/gpfs/lsawade/SpecfemMagic/specfem3d_globe"

if __name__ == '__main__':
    p = Pipeline()

    # Hello World########################################################
    test_stage = Stage()
    test_stage.name = "HelloWorldStage"

    # Create 'Hello world' task
    t = Task()
    t.pre_exec = ['module load openmpi/gcc']
    t.name = "HelloWorldTask"
    t.executable = '/bin/echo'
    t.arguments = ['"Hello world"']
    t.stdout = 'STDOUT'
    t.stderr = 'STDERR'
    t.download_output_data = ['STDOUT', 'STDERR']

    # Add task to stage and stage to pipeline
    test_stage.add_tasks(t)
    p.add_stages(test_stage)

    # # Download ########################################################
    # s = Stage()
    # s.name = 'DownloadStage'

    # # Create a Task object
    # t = Task()
    # t.name = 'DownloadTask'        # Assign a name to the task (optional, do not use ',' or '_')
    # t.executable = '/usr/bin/ssh'
    # t.arguments = ["lsawade@traverse.princeton.edu","'bash -l /home/lsawade/gcmt3d/workflow/entk/ssh-request-data.sh /tigress/lsawade/source_inversion_II/events/CMT.perturb.440/C200605061826B /home/lsawade/gcmt3d/workflow/params'"]
    # t.download_output_data = ['STDOUT', 'STDERR']
    # t.cpu_reqs = {
    #     'cpu_processes': 1,
    #     'cpu_process_type': None,
    #     'cpu_threads': 1,
    #     'cpu_thread_type': None
    # }

    # # Add Task to Stage and Stage to the Pipeline
    # s.add_tasks(t)
    # p.add_stages(s)

       
    specfem_stage = Stage()
    specfem_stage.name = 'SimulationStage'
    
    for i in range(2):

        # Create Task
        t = Task()
        t.name = f"SIMULATION.{i}"
        tdir = f"/home/lsawade/simple_entk_specfem/specfem_run_{i}"
        t.pre_exec = [
            # Load necessary modules
            'module load openmpi/gcc',
            'module load cudatoolkit',
            
            # Change to your specfem run directory
            f'rm -rf {tdir}',
            f'mkdir {tdir}',
            f'cd {tdir}',
            
            # Create data structure in place
            f'ln -s {specfem}/bin .',
            f'ln -s {specfem}/DATABASES_MPI .',
            f'cp -r {specfem}/OUTPUT_FILES .',
            'mkdir DATA',
            f'cp {specfem}/DATA/CMTSOLUTION ./DATA/',
            f'cp {specfem}/DATA/STATIONS ./DATA/',
            f'cp {specfem}/DATA/Par_file ./DATA/'
        ]
        t.executable = './bin/xspecfem3D'
        t.cpu_reqs = {'cpu_processes': 4, 'cpu_process_type': 'MPI', 'cpu_threads': 1, 'cpu_thread_type' : 'OpenMP'}
        t.gpu_reqs = {'gpu_processes': 1, 'gpu_process_type': None, 'gpu_threads': 1, 'gpu_thread_type' : 'CUDA'}
        t.stdout = 'STDOUT'
        t.stderr = 'STDERR'
        t.download_output_data = ['STDOUT', 'STDERR']

        # Add task to stage
        specfem_stage.add_tasks(t)
        
    # p.add_stages(specfem_stage)
        
    res_dict = {
        'resource': 'princeton.traverse', # 'local.localhost',
        'schema'   : 'local',
        'walltime':  20, #2 * 30,
        'cpus': 2 * 4 + 4,
        'gpus': 2 * 4,          
    }

    appman = AppManager(hostname=hostname, port=port, username=username, password=password, resubmit_failed=False)
    appman.resource_desc = res_dict
    appman.workflow = set([p])
    appman.run()        
    
