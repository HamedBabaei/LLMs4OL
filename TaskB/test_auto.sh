#!/bin/bash

label="nofinetuning"
device="cpu"
datasets=("geonames" "umls" "schema")
templates=("0" "1" "2" "3" "4" "5" "6" "7")
models=("bert_large" "flan_t5_large" "flan_t5_xl" "bart_large" "gpt2_large" "gpt2_xl" "gpt3" "gpt3_ada")
for kb_name in "${datasets[@]}"; do
  index=1
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${templates[@]}"; do
      echo "Running on dataset: $kb_name , model: $model_name, template: $template!"
      python3 test.py --kb_name=$kb_name --model=$model_name --template=$template --device=$device
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done

