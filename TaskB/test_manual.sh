#!/bin/bash
read -p "Enter dataset out of (geonames, umls, schema):" kb_name

read -p "Enter output logs path for $kb_name results:" log

read -p "Enter the name of model out of (bert_large, flan_t5_large, flan_t5_xl, bart_large, gpt2_large, gpt2_xl, gpt3, gpt3_ada, bloom_1b7, bloom_3b, bloom_7b1, llama_7b, gpt4, chatgpt):" model_name

read -p "Enter the device (cpu, cuda, cuda:1, cuda:2, ...):" device

exec > $log

echo "Running baseline models!"

templates=("1" "2" "3" "4" "5" "6" "7" "8")

for template in "${templates[@]}"; do
  echo "Running $model_name for template: $template!"
  python3 test.py --kb_name=$kb_name --model=$model_name --template=$template --device=$device
  echo "Inference for  $model_name on template: $template  is done"
  echo "-----------------------------------------------------------"
done
