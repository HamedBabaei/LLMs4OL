# #!/bin/bash

label="fewshot"
device="cuda"
task_a_templates=("template-1" "template-2" "template-3" "template-4" "template-5" "template-6" "template-7" "template-8")
task_b_templates=("0" "1" "2" "3" "4" "5" "6" "7")

#-------------------------------------FLAN-T5-Large and XL--------WN18RR---------------------------------------------------------
# running models for WN18RR
python trainer.py --kb_name="wn18rr" --model_to_train="flan_t5_large" --num_train_epochs=10
python trainer.py --kb_name="wn18rr" --model_to_train="flan_t5_xl" --num_train_epochs=10

cd ..
cd TaskA

datasets=("wn18rr")
models=("wn18rr_flan_t5_large" "wn18rr_flan_t5_xl")

for kb_name in "${datasets[@]}"; do
  index=11
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_a_templates[@]}"; do
      echo "Running on dataset: $kb_name , model: $model_name, template: $template!"
      python3 test.py --kb_name=$kb_name --model_name=$model_name --template=$template --device=$device
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done

cd ..
cd tuning

#-------------------------------------FLAN-T5-Large--------UMLS---------------------------------------------------------
# running models for UMLS

python trainer.py --kb_name="umls" --model_to_train="flan_t5_large" --num_train_epochs=10

cd ..
cd TaskA

datasets=("nci" "snomedct_us" "medcin")
models=("umls_flan_t5_large")

for kb_name in "${datasets[@]}"; do
  index=8
  for model_name in "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_a_templates[@]}"; do
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

datasets=("umls")

for kb_name in "${datasets[@]}"; do
  index=8
  for model_name in "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_b_templates[@]}"; do
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

for kb_name in "${datasets[@]}"; do
  index=8
  for model_name in "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    echo "Running on dataset: $kb_name , model: $model_name !"
    python3 test.py --kb_name=$kb_name --model=$model_name --device=$device
    echo "Inference for  $model_name  is done"
    echo "-----------------------------------------------------------"
    index=$((index+1))
  done
done


cd ..
cd tuning

#-------------------------------------FLAN-T5-XL--------UMLS---------------------------------------------------------
# running models for UMLS

python trainer.py --kb_name="umls" --model_to_train="flan_t5_xl" --num_train_epochs=10

cd ..
cd TaskA

datasets=("nci" "snomedct_us" "medcin")
models=("umls_flan_t5_xl")

for kb_name in "${datasets[@]}"; do
  index=9
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_a_templates[@]}"; do
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

datasets=("umls")

for kb_name in "${datasets[@]}"; do
  index=9
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_b_templates[@]}"; do
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

for kb_name in "${datasets[@]}"; do
  index=2
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

cd ..
cd tuning

#-------------------------------------FLAN-T5-Large--------GeoNames---------------------------------------------------------
# running models for GeoNames

python trainer.py --kb_name="geonames" --model_to_train="flan_t5_large" --num_train_epochs=10

cd ..
cd TaskB

datasets=("geonames")
models=("geonames_flan_t5_large")

for kb_name in "${datasets[@]}"; do
  index=8
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_b_templates[@]}"; do
      echo "Running on dataset: $kb_name , model: $model_name, template: $template!"
      python3 test.py --kb_name=$kb_name --model=$model_name --template=$template --device=$device
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done

cd ..
cd TaskA

for kb_name in "${datasets[@]}"; do
  index=8
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_a_templates[@]}"; do
      echo "Running on dataset: $kb_name , model: $model_name, template: $template!"
      python3 test.py --kb_name=$kb_name --model_name=$model_name --template=$template --device=$device
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done

cd ..
cd tuning

#-------------------------------------FLAN-T5-XL--------GeoNames---------------------------------------------------------
# running models for GeoNames

python trainer.py --kb_name="geonames" --model_to_train="flan_t5_xl" --num_train_epochs=10


cd ..
cd TaskB

models=("geonames_flan_t5_xl")

for kb_name in "${datasets[@]}"; do
  index=9
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_b_templates[@]}"; do
      echo "Running on dataset: $kb_name , model: $model_name, template: $template!"
      python3 test.py --kb_name=$kb_name --model=$model_name --template=$template --device=$device
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done

cd ..
cd TaskA

for kb_name in "${datasets[@]}"; do
  index=9
  for model_name in  "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_a_templates[@]}"; do
      echo "Running on dataset: $kb_name , model: $model_name, template: $template!"
      python3 test.py --kb_name=$kb_name --model_name=$model_name --template=$template --device=$device
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done


#-------------------------------------FLAN-T5-Large--------SCHEMA---------------------------------------------------------
# running models for SchemaORG
python trainer.py --kb_name="schemaorg" --model_to_train="flan_t5_large" --num_train_epochs=5

cd ..
cd TaskB
datasets=("schema")
models=("schemaorg_flan_t5_large")

for kb_name in "${datasets[@]}"; do
  index=8
  for model_name in "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_b_templates[@]}"; do
      echo "Running on dataset: $kb_name , model: $model_name, template: $template!"
      python3 test.py --kb_name=$kb_name --model=$model_name --template=$template --device=$device
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done

cd ..
cd tuning

#-------------------------------------FLAN-T5-XL--------SCHEMA---------------------------------------------------------
# running models for SchemaORG
python trainer.py --kb_name="schemaorg" --model_to_train="flan_t5_xl" --num_train_epochs=5

cd ..
cd TaskB
models=("schemaorg_flan_t5_xl")

for kb_name in "${datasets[@]}"; do
  index=9
  for model_name in "${models[@]}"; do
    log="results/$kb_name/$index-$kb_name-$model_name.$label.test.log.txt"
    exec > $log
    for template in "${task_b_templates[@]}"; do
      echo "Running on dataset: $kb_name , model: $model_name, template: $template!"
      python3 test.py --kb_name=$kb_name --model=$model_name --template=$template --device=$device
      echo "Inference for  $model_name on template: $template  is done"
      echo "-----------------------------------------------------------"
    done
    index=$((index+1))
  done
done

