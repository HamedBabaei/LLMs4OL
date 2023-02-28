#!/bin/bash
read -p "Enter gpu name >>> " $gpu

read -p "Enter user name >>> " $user

docker build -f Dockerfile . -t llms4ol

docker save -o assets/llms4ol.tar llms4ol

singularity build assets/llms4ol.sif docker-archive:assets/llms4ol.tar

srun -w devbox5 --gres=gpu:$gpu:1 singularity exec -B /nfs/home/$user/:/run/user assets/llms4ol.sif jupyter-lab

