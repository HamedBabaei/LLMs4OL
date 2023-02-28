#!/bin/bash

read -p "Enter gpu name >>> " $gpu

read -p "Enter user name >>> " $user

srun -w devbox5 --gres=gpu:$gpu:1 singularity exec -B /nfs/home/$user/:/run/user llms4ol.sif jupyter-lab
