#!/bin/bash

#SBATCH --nodes=2
#SBATCH --ntasks=6
#SBATCH --ntasks-per-node=3
#SBATCH --mem=40000
#SBATCH --gres=gpu:3
#SBATCH --time 00:30:00
#SBATCH -p pReserved

# load modules
module load intel
module load openmpi
module load cudatoolkit/10.0

# Define your specfem run directory
cd <your_specfem_run_dir>

# change directory to build
ln -s /tigress/lsawade/specfem3d_globe/bin .
ln -s /tigress/lsawade/specfem3d_globe/DATABASES_MPI .
cp -s /tigress/lsawade/specfem3d_globe/OUTPUT_FILES .
cp -s /tigress/lsawade/specfem3d_globe/DATA .


# Run Mesher
srun ./bin/xmeshfem3D

# Run Solver
srun ./bin/xspecfem3D
