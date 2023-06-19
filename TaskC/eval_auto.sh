#!/bin/bash

label="nofinetuning"

datasets=("umls")
templates=("-0-")
models=("gpt3" "gpt4")

for kb_name in "${datasets[@]}"; do
  index=7
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${templates[@]}"; do
      echo "Running on dataset: $kb_name , model: $model_name, template: $template!"
      python3 evaluator.py --kb_name=$kb_name --model=$model_name --template=$template
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done
