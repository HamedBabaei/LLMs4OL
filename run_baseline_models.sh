#!/bin/bash
echo "Enter dataset out of (wn18rr, geonames, nci):"
read kb_name

echo "Enter output logs path for $kb_name results:"
read log

echo "Enter the name of model out of (bert_large):"
read model_name

exec > $log

echo "Running baseline models!"

templates=("template-1" "template-2" "template-3" "template-4" "template-5" "template-6" "template-7" "template-8")
for template in "${templates[@]}"; do
  echo "Running $model_name for template: $template!"
  python3 run_baseline_models.py --kb_name=$kb_name --model_name=$model_name --template=$template
  echo "Inference for  $model_name on template: $template  is done"
  echo "-----------------------------------------------------------"
done
