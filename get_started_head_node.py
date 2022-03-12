from radical.entk import Pipeline, Stage, Task, AppManager
1;95;0cimport os

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

# Description of how the RabbitMQ process is accessible
# No need to change/set any variables if you installed RabbitMQ has a system
# process. If you are running RabbitMQ under a docker container or another
# VM, set "RMQ_HOSTNAME" and "RMQ_PORT" in the session where you are running
# this script.
hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = int(os.environ.get('RMQ_PORT', 5672))
password = os.environ.get('RMQ_PASSWORD', None)
username = os.environ.get('RMQ_USERNAME', None)

print(hostname, port, username, password)

if __name__ == '__main__':

    # Create a Pipeline object
    p = Pipeline()

    # Create a Stage object
    s = Stage()

    # # Create a Task object
    # t = Task()
    # t.name = 'my-first-task'        # Assign a name to the task (optional, do not use ',' or '_')
    # t.pre_exec = ["echo Hi"]
    # t.executable = '/bin/echo'   # Assign executable to the task
    # t.arguments = ['Lol if this works, that would be ridiculous']  # Assign arguments for the task executable
    # t.download_output_data = ['STDOUT', 'STDERR']
    # t.cpu_reqs = {
    #     'processes': 1,
    #     'process_type': 'MPI',
    #     'threads_per_process': 1,
    #     'thread_type': 'OpenMP'}

    # # Add Task to the Stage
    # s.add_tasks(t)

    # # Add Stage to the Pipeline
    # p.add_stages(s)

    # Create a Task object
    t = Task()
    t.name = 'my-first-task'        # Assign a name to the task (optional, do not use ',' or '_')
    t.pre_exec = ["echo Im gonna download hopefully",
                  "echo IP: $RP_APP_TUNNEL_ADDR"]
    t.executable = '/bin/ssh' # Assign executable to the task
    t.arguments = ['$RP_APP_TUNNEL_ADDR',
                   'bash', '-l',
                   '/home/lsawade/gcmt3d/workflow/entk/ssh-request-data.sh',
                   '/tigress/lsawade/source_inversion_II/events/CMT.perturb.440/C200605061826B',
                   '/home/lsawade/gcmt3d/workflow/params'
                    ]  # Assign arguments for the task executable

    t.download_output_data = ['STDOUT', 'STDERR']
    t.cpu_reqs = {
        'processes': 1,
        'process_type': 'MPI',
        'threads_per_process': 1,
        'thread_type': 'OpenMP'}
        # Add Task to the Stage
    s.add_tasks(t)

    # Add Stage to the Pipeline
    p.add_stages(s)
    
    # Create Application Manager
    appman = AppManager(hostname=hostname, port=port, username=username, password=password)

    # Create a dictionary describe four mandatory keys:
    # resource, walltime, and cpus
    # resource is 'local.localhost' to execute locally
    res_dict = {

        'resource':  'princeton.traverse',
        # 'queue'   : 'rh8',
        'project_id': 'test',
        'schema'   : 'local',
        'walltime': 5,
        'cpus': 32 * 1,
        'gpu': 4 * 1
    }

    # Assign resource request description to the Application Manager
    appman.resource_desc = res_dict

    # Assign the workflow as a set or list of Pipelines to the Application Manager
    # Note: The list order is not guaranteed to be preserved
    appman.workflow = set([p])

    # Run the Application Manager
    appman.run()
