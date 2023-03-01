#!/bin/bash

label="nofinetuning"
datasets=("wn18rr" "geonames" "nci" "snomedct_us" "medcin")
templates=("template-1" "template-2" "template-3" "template-4" "template-5" "template-6" "template-7" "template-8")
models=("bert_large" "flan_t5_large" "flan_t5_xl")

for kb_name in "${datasets[@]}"; do
  index=1
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${templates[@]}"; do
      echo "Running $model_name for template: $template!"
      echo "$kb_name-$model_name-$template.log"
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done