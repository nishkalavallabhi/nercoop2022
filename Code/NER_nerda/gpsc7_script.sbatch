#!/bin/bash
#SBATCH --account=nrc_ict__gpu_a100
#SBATCH --qos=low
#SBATCH --job-name=GPU-Mbert-Conll_nl-fine_tuning
#SBATCH --output=%x-%j.out
#SBATCH --partition=gpu_a100
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --gpus-per-task=1
#SBATCH --comment="image=nrc/nrc_all_default_ubuntu-18.04-amd64_latest"

export LD_LIBRARY_PATH=/home/aks000/u/miniconda3/envs/hgf/lib:$LD_LIBRARY_PATH
python sub_script.py
