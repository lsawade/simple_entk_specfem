# Simple testing repo to set up EnTK with `specfem3d_globe`


## SUMMIT


### First simple test to get running

Get interactive job allocation with SMT1 (no jobs make use of simultaneous hardware threads)

```bash
bsub -W 2:00 -nnodes 1 -P GEO111 -alloc_flags "gpumps smt1" -Is /bin/bash
```

Once you have the allocation load the right modules etc.
```bash
module load gcc/7.5.0 spectrum-mpi cuda cmake boost

# OR(!)
cd /gpfs/alpine/geo111/scratch/lsawade/SpecfemMagic
source 00_compilations_parameters.sh 
cd - 
```

Then, go into specfem directory
```bash
cd /gpfs/alpine/geo111/scratch/lsawade/SpecfemMagic/specfem3d_globe
```
and launch specfem
```bash
jsrun -n6 -a4 -c4 -g1 ./bin/xspecfem3D &
```

The code takes about 40 seconds. It uses a total of
24 MPI tasks, divided into 6 resource sets of 4 CPUS + 1 GPU,
where each GPU takes 4 MPI tasks.

You can monitor progress using
```bash
tail -f OUTPUT_FILES/output_solver.txt
```



### Create new specfem simulation directories and run those

This is a task that the workflow manager will do all the time and
the crux of the workflow. Meaning, if we get this into EnTK form,
we are golden.

Get interactivae allocation with two nodes so that we can run two
specfems in parallel:
```bash
bsub -W 2:00 -nnodes 2 -P GEO111 -alloc_flags "gpumps smt1" -Is /bin/bash
```

First, define a location where you want to create simulation directories

```bash
TESTDIR=/gpfs/alpine/geo111/scratch/lsawade/entk_test
mkdir $TESTDIR
```

If you have runs from before just remove them
```bash
rm -rf ${TESTDIR}/*
```

Then, changed the variable specfem
```bash
mkspecfemdirs $TESTDIR
```

Now, that we have created the directories we can run the two specfems

```bash
for RUNDIR in $(ls $TESTDIR)
do
    cd ${TESTDIR}/${RUNDIR}
    jsrun -n6 -a4 -c4 -g1 ./bin/xspecfem3D &
    cd -
done
```

Or, as a one-liner:
```bash
for RUNDIR in $(ls $TESTDIR); do cd ${TESTDIR}/${RUNDIR}; jsrun -n6 -a4 -c4 -g1 ./bin/xspecfem3D & cd -; done;
```

You can monitor the progress using
```bash
# For run 1
tail -f ${TESTDIR}/specfem_run_1/OUTPUT_FILES/output_solver.txt

# For run 2
tail -f ${TESTDIR}/specfem_run_2/OUTPUT_FILES/output_solver.txt
```



The creation of the specfem directories is controlled by an executable from
my software, which could be run as a pre-task or a task, does not really matter.







---

Below not relevant at the moment.

## TIGER/TRAVERSE


There are the main files. The EnTK pipeline `solver.py`, the respective, 
working slurmscript and the `.entkrc` which is `source`'ed before running
anything, so that all environment variables and modules are in place.

The working `specfem3d_globe` repository is located here
```bash
/tigress/lsawade/specfem3d_globe
```


## Running the pipeline

To run the pipeline, I follow this sequence of commands:

```bash

# Setup environment variables
source .entkrc

# Activate EnTK environment
conda activate entk

# Run the pipeline
python solver.py

```

