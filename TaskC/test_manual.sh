#!/bin/bash
read -p "Enter dataset out of (umls):" kb_name

read -p "Enter output logs path for $kb_name results:" log

read -p "Enter the name of model out of (bert_large, flan_t5_large, flan_t5_xl, bart_large, gpt3, gpt3_ada, bloom_1b7, bloom_3b, bloom_7b1):" model_name

read -p "Enter the device (cpu, cuda, cuda:1, cuda:2, ...):" device

exec > $log


echo "Running baseline models!"

echo "Running $model_name !"
python3 test.py --kb_name=$kb_name --model=$model_name --device=$device
echo "Inference for  $model_name is done"
echo "-----------------------------------------------------------"
