#!/bin/bash

label="nofinetuning"
device="cpu"
datasets=("umls")
models=("bert_large" "flan_t5_large" "flan_t5_xl" "bart_large" "gpt2_large" "gpt2_xl" "gpt3" "gpt3_ada" "bloom_1b7" "bloom_3b" "bloom_7b1")
for kb_name in "${datasets[@]}"; do
  index=1
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    echo "Running on dataset: $kb_name , model: $model_name !"
    python3 test.py --kb_name=$kb_name --model=$model_name --device=$device
    echo "Inference for  $model_name  is done"
    echo "-----------------------------------------------------------"
    index=$((index+1))
  done
done
