#!/bin/bash
#SBATCH --account=nrc_ict__gpu_v100
#SBATCH --qos=normal
#SBATCH --job-name=GPU-Xlm-fine_tuning
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=gpu_v100
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=84G
#SBATCH --gpus-per-task=1
#SBATCH --comment="image=nrc/nrc_all_default_ubuntu-18.04-amd64_latest"

python sub_script.py

