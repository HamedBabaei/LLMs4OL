#!/bin/bash

# FSL
# ------------------------
python trainer.py --kb_name="wn18rr" --model_to_train="flan_t5_large"
#parser.add_argument("--kb_name", required=True)  # wn18rr, geonames, umls
#parser.add_argument("--model_to_train", required=True) # flan_t5_large, flan_t5_xl

cd ..
cd TaskA

label="nofinetuning"
device="cpu"
datasets=("wn18rr" "geonames" "nci" "snomedct_us" "medcin")
templates=("template-1" "template-2" "template-3" "template-4" "template-5" "template-6" "template-7" "template-8")
models=("flan-t5-large" "flan-t5-xl")

for kb_name in "${datasets[@]}"; do
  index=1
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${templates[@]}"; do
      echo "Running on dataset: $kb_name , model: $model_name, template: $template!"
      python3 test.py --kb_name=$kb_name --model_name=$model_name --template=$template --device=$device
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done


cd ..
cd TaskB
label="nofinetuning"
device="cpu"
datasets=("geonames" "umls" "schema")
templates=("0" "1" "2" "3" "4" "5" "6" "7")
models=("bert_large" "flan_t5_large" "flan_t5_xl" "bart_large" "gpt2_large" "gpt2_xl" "gpt3" "gpt3_ada" "bloom_1b7" "bloom_3b" "bloom_7b1")
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


cd ..
cd TaskC


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
