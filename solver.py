from radical.entk import Pipeline, Stage, Task, AppManager
import traceback, sys, os

os.environ['RADICAL_PILOT_DBURL'] = "mongodb://user:user123@ds043012.mlab.com:43012/princeton"
os.environ['RMQ_HOSTNAME'] = "two.radical-project.org"
os.environ['RMQ_PORT'] = "33267"

hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = os.environ.get('RMQ_PORT', 5672)

if __name__ == '__main__':
    p = Pipeline()

    specfem_stage = Stage()

    t1 = Task()
    t1.pre_exec = [
        'module purge',
        'module load intel',
        'module load openmpi',
        'module load cudatoolkit/10.0',
        'ln -s /tigress/lsawade/specfem3d_globe/DATA .',
        'ln -s /tigress/lsawade/specfem3d_globe/bin .',
        'cp -r /tigress/lsawade/specfem3d_globe/OUTPUT_FILES ./',
        'ln -s /tigress/lsawade/specfem3d_globe/DATABASES_MPI .'
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

    
