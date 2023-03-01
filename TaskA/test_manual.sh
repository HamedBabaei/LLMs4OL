#!/bin/bash
read -p "Enter dataset out of (wn18rr, geonames, nci, snomedct_us, medcin):" kb_name

read -p "Enter output logs path for $kb_name results:" log

read -p "Enter the name of model out of (bert_large, flan_t5_large, flan_t5_xl):" model_name

exec > $log

echo "Running baseline models!"

templates=("template-1" "template-2" "template-3" "template-4" "template-5" "template-6" "template-7" "template-8")

for template in "${templates[@]}"; do
  echo "Running $model_name for template: $template!"
  python3 level1_inference_runner.py --kb_name=$kb_name --model_name=$model_name --template=$template
  echo "Inference for  $model_name on template: $template  is done"
  echo "-----------------------------------------------------------"
done
