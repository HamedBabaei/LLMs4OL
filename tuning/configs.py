import argparse
import datetime
import os
import torch


class BaseConfig:
    def __init__(self, n_per_class=8, neg_per_class=3):
        self.root_dir = "../datasets/Tuning"
        self.llms_root_dir = "../assets/Tuning"
        self.parser = argparse.ArgumentParser()
        self.dataset_dir_getter = {
            "wn18rr": "WN18RR",
            "geonames": "Geonames",
            "umls": "NCI",
            "schemaorg":"SCHEMA"
        }
        self.n_per_class = n_per_class
        self.neg_per_class = neg_per_class

    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def get_args(self, kb_name: str, model_to_train: str=None):
        # kb_names = [wn18rr, geonames, umls]
        dataset_dir = self.dataset_dir_getter.get(kb_name)
        self.parser.add_argument("--kb_name", type=str, default=kb_name)

        # BUILD_DATASET CONFIG
        if dataset_dir == "NCI":
            self.parser.add_argument("--entity_path", type=str, default=f"../datasets/TaskA/{kb_name.upper()}/{dataset_dir.lower()}_entities.json")
            self.parser.add_argument("--label_mapper", type=str, default=f"../datasets/TaskA/{kb_name.upper()}/label_mapper.json")
            self.parser.add_argument("--biorel_dir", type=str, default=f"../datasets/TaskA/{kb_name.upper()}/raw/biorel")
        else:
            self.parser.add_argument("--entity_path", type=str, default=f"../datasets/TaskA/{dataset_dir}/{kb_name}_entities.json")
            self.parser.add_argument("--label_mapper", type=str, default=f"../datasets/TaskA/{dataset_dir}/label_mapper.json")

        self.parser.add_argument("--umls_task_b_train", type=str, default=f"../datasets/TaskB/UMLS/processed/hierarchy_train.json")
        self.parser.add_argument("--umls_task_c_train", type=str, default=f"../datasets/TaskC/UMLS/processed/graph_sn_dict_train.json")
        self.parser.add_argument("--geonames_task_b_train", type=str, default=f"../datasets/TaskB/Geonames/processed/hierarchy_train.json")
        self.parser.add_argument("--schema_task_b_train", type=str, default=f"../datasets/TaskB/SchemaOrg/processed/hierarchy_train.json")
        if dataset_dir=="SCHEMA":
            self.parser.add_argument("--fsl_train_data", type=str, default=f"../datasets/TaskB/SchemaOrg/processed/hierarchy_train.json")
        else:
            self.parser.add_argument("--fsl_train_data", type=str, default=f"{self.root_dir}/{kb_name}-{self.n_per_class}-shot-{str(self.neg_per_class)}-neg.json")
        self.parser.add_argument("--n_per_class", type=int, default=self.n_per_class)
        self.parser.add_argument("--neg_per_class", type=int, default=self.neg_per_class)
        self.parser.add_argument("--seed", type=int, default=555)


        # TRAINING CONFIG
        self.parser.add_argument("--max_source_length", type=int, default=512)
        self.parser.add_argument("--max_target_length", type=int, default=10)
        self.parser.add_argument("--label_pad_token_id", type=int, default=-100)
        self.parser.add_argument("--auto_find_batch_size", type=bool, default=True)
        self.parser.add_argument("--learning_rate", type=float, default=1e-5)
        self.parser.add_argument("--num_train_epochs", type=int, default=5)

        time = str(datetime.datetime.now()).split('.')[0]

        if model_to_train == "flan_t5_large":
            self.parser.add_argument("--model_input_path", type=str, default="../assets/LLMs/flan-t5-large")
            self.parser.add_argument("--model_output_path", type=str,  default=f"../assets/Tuning/{kb_name}-flan-t5-large")
            self.parser.add_argument("--output_log_dir", type=str, default=f"../assets/Tuning/{kb_name}-flan-t5-large-log")
            self.parser.add_argument("--model_to_train", type=str, default="flan_t5_large")

        if model_to_train == "flan_t5_xl":
            self.parser.add_argument("--model_input_path", type=str, default="../assets/LLMs/flan-t5-xl")
            self.parser.add_argument("--model_output_path", type=str,  default=f"../assets/Tuning/{kb_name}-flan-t5-xl")
            self.parser.add_argument("--output_log_dir", type=str, default=f"../assets/Tuning/{kb_name}-flan-t5-xl-log")
            self.parser.add_argument("--model_to_train", type=str, default="flan_t5_xl")

        self.parser.add_argument("--gpu_no", type=int, default=torch.cuda.device_count())
        self.parser.add_argument("-f")
        return self.parser.parse_args()

