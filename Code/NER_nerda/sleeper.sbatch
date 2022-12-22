#!/bin/bash
#SBATCH --account=nrc_ict__gpu_v100
#SBATCH --qos=normal
#SBATCH --job-name=GPU-AdvFinetune
#SBATCH --output=%x-%j.out
#SBATCH --partition=gpu_v100
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --gpus-per-task=1
#SBATCH --comment="image=nrc/nrc_all_default_ubuntu-18.04-amd64_latest"


echo "Sleeping for 10000 seconds..." 
sleep 10000
