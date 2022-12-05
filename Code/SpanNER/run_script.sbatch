#!/bin/bash
#SBATCH --job-name=GPU-A100-Conll_deu_0%
#SBATCH --partition=gpu_a100
#SBATCH --account=nrc_ict__gpu_a100
#SBATCH --qos=low
#SBATCH --time=2880
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=122880M
#SBATCH --gres=gpu:1

#SBATCH --comment="image=nrc/nrc_all_default_ubuntu-18.04-amd64_latest"
#SBATCH --open-mode=append

#SBATCH --signal=B:15@30


export LD_LIBRARY_PATH=/home/aks000/u/miniconda3/envs/hgf/lib:$LD_LIBRARY_PATH
python evaluate.py

