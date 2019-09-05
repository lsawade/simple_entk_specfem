from radical.entk import Pipeline, Stage, Task, AppManager
import traceback, sys, os


hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = os.environ.get('RMQ_PORT', 5672)

if __name__ == '__main__':
    p = Pipeline()

    specfem_stage = Stage()

    t1 = Task()
    t1.pre_exec = [
        # Load necessary modules
        'module purge',
        'module load intel',
        'module load openmpi',
        'module load cudatoolkit/10.0',
        
        # Change to your specfem run directory
        'cd /home/lsawade/specfem_run',
        
        # Create data structure in place
        'ln -s /scratch/gpfs/lsawade/specfem3d_globe_gpu/bin .',
        'ln -s /scratch/gpfs/lsawade/specfem3d_globe_gpu/DATABASES_MPI .',
        'cp -r /scratch/gpfs/lsawade/specfem3d_globe_gpu/OUTPUT_FILES .',
        'cp -r /scratch/gpfs/lsawade/specfem3d_globe_gpu/DATA .'
    ]
    t1.executable = ['./bin/xspecfem3D']
    t1.cpu_reqs = {'processes': 6, 'process_type': 'MPI', 'threads_per_process': 1, 'thread_type': 'OpenMP'}
    t1.gpu_reqs = {'processes': 6, 'process_type': 'MPI', 'threads_per_process': 1, 'thread_type': 'OpenMP'}
    t1.download_output_data = ['STDOUT', 'STDERR']

    specfem_stage.add_tasks(t1)

    p.add_stages(specfem_stage)

    res_dict = {
                'resource': 'princeton.tiger_gpu',
                'project' : 'geo',
                'queue'   : 'gpu',
                'schema'   : 'local',
                # Here we specifify walltime, which is the total exectution of
                # EnTK. But time in the queue seems to not be considered?
                #Is that correct?
                'walltime': 30,
                'gpus': 6,
                'cpus': 6
    }
    

    try:

        appman = AppManager(hostname=hostname, port=port, resubmit_failed=False)
        appman.resource_desc = res_dict
        appman.workflow = set([p])
        appman.run()        

    except Exception, ex:

        print 'Execution failed, error: %s'%ex
        print traceback.format_exc()

    
