#!/bin/bash

label="nofinetuning"

datasets=("wn18rr" "geonames" "nci" "snomedct_us" "medcin")
templates=("template-1" "template-2" "template-3" "template-4" "template-5" "template-6" "template-7" "template-8")
models=("gpt3" "bloom_1b7" "bloom_3b" "chatgpt" "llama_7b" "gpt4")

for kb_name in "${datasets[@]}"; do
  index=6
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


label="zeroshot"
datasets=("geonames")
models=("geonames_flan_t5_large" "geonames_flan_t5_xl")

for kb_name in "${datasets[@]}"; do
  index=8
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
