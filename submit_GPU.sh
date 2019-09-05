#!/bin/bash

#SBATCH --nodes=2
#SBATCH --ntasks=6
#SBATCH --ntasks-per-node=3
#SBATCH --mem=40000
#SBATCH --gres=gpu:3
#SBATCH --time 00:30:00
#SBATCH -p pReserved

module purge
# load modules
module load intel
module load openmpi
module load cudatoolkit/10.0

# Define your specfem run directory
cd /home/lsawade/specfem_run

# Copy and link files
ln -s /scratch/gpfs/lsawade/specfem3d_globe_gpu/bin .
ln -s /scratch/gpfs/lsawade/specfem3d_globe_gpu/DATABASES_MPI .
cp -r /scratch/gpfs/lsawade/specfem3d_globe_gpu/OUTPUT_FILES .
cp -r /scratch/gpfs/lsawade/specfem3d_globe_gpu/DATA .


# Run Mesher
srun ./bin/xmeshfem3D

# Run Solver
srun ./bin/xspecfem3D
