import argparse
import datetime
import os
import torch


class BaseConfig:
    def __init__(self, plm="flan-t5-xl"):
        self.root_dir = "../datasets/FSL"
        self.llms_root_dir = "../assets/FSL/"
        self.parser = argparse.ArgumentParser()
        self.dataset_dir_getter = {
            "wn18rr": "WN18RR",
            "geonames": "Geonames",
            "umls": "UMLS"
        }

    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def get_args(self, kb_name: str):
        # kb_names = [wn18rr, geonames, umls]
        dataset_dir = self.dataset_dir_getter.get(kb_name)
        # BUILD_DATASET CONFIG
        self.parser.add_argument("--entity_path", type=str, default=f"../datasets/TaskA/{dataset_dir}/{kb_name}_entities.json")
        self.parser.add_argument("--label_mapper", type=str, default=f"../datasets/TaskA/{dataset_dir}/label_mapper.json")
        self.parser.add_argument("--plm_train_data", type=str, default=f"{self.root_dir}/{dataset_dir}_data.json")

        self.parser.add_argument("--n_per_class", type=int, default=8)
        self.parser.add_argument("--neg_per_class", type=int, default=4)
        self.parser.add_argument("--seed", type=int, default=555)

        # TRAINING CONFIG
        self.parser.add_argument("--max_source_length", type=int, default=512)
        self.parser.add_argument("--max_target_length", type=int, default=10)

        time = str(datetime.datetime.now()).split('.')[0]

        if model == "flan_t5_large":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/flan-t5-large")
            self.parser.add_argument("--template_name", type=str, default="t5")
            self.parser.add_argument("--multi_gpu", type=bool, default=True)
        if model == "flan_t5_xl":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/flan-t5-xl")
            self.parser.add_argument("--template_name", type=str, default="t5")
            self.parser.add_argument("--multi_gpu", type=bool, default=True)

        self.parser.add_argument("--gpu_no", type=int, default=torch.cuda.device_count())
        self.parser.add_argument("-f")
        return self.parser.parse_args()

