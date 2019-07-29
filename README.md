# Simple testing repo for a Specfem Run on the TigerGPU cluster


There are the main files. The EnTK pipeline `solver.py`, the respective, 
working slurmscript and the `.entkrc` which is `source`'ed before running
anything, so that all environment variables and modules are in place.

The working `specfem3d_globe` repository is located in here
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

