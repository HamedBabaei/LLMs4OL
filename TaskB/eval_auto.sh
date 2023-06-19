#!/bin/bash

label="nofinetuning"

datasets=("geonames" "schema" "umls")
templates=("-0-" "-1-" "-2-" "-3-" "-4-" "-5-" "-6-" "-7-")
models=("gpt3" "gpt4" "chatgpt")

for kb_name in "${datasets[@]}"; do
  index=1
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
