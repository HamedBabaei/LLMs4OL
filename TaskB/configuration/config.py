"""
    DataConfig: Data Configuration of models
"""
import argparse
import datetime
import os

class BaseConfig:
    """
        Base Configs
    """
    def __init__(self):
        """
            Data configuration
        """
        self.parser = argparse.ArgumentParser()
        self.argument_getter = {
            "geonames": ["Geonames", self.add_geoname],
            "umls":["UMLS", self.add_umls],
            "schema":["SchemaOrg", self.add_schema]
        }
        self.root_dir = "../datasets/TaskB"
        self.llms_root_dir = "../assets/LLMs"
        
    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
            
    def add_geoname(self, dataset: str):
        self.parser.add_argument("--raw_feature_codes", type=str, default=f"{self.root_dir}/{dataset}/raw/featureCodes_en.txt")
        self.parser.add_argument("--feature_codes", type=str, default=f"{self.root_dir}/{dataset}/processed/feature_codes.csv")

    def add_umls(self, dataset: str):
        self.parser.add_argument("--raw_sn_nci", type=str, default=f"{self.root_dir}/{dataset}/raw/nci_semantic_network.json")
        self.parser.add_argument("--raw_sn_medcin", type=str, default=f"{self.root_dir}/{dataset}/raw/medcin_semantic_network.json")
        self.parser.add_argument("--raw_sn_snomedct_us", type=str, default=f"{self.root_dir}/{dataset}/raw/snomedct_us_semantic_network.json")
        self.parser.add_argument("--raw_sn", type=str, default=f"{self.root_dir}/{dataset}/raw/semantic_network.json")
        self.parser.add_argument("--processed_sn", type=str, default=f"{self.root_dir}/{dataset}/processed/semantic_network.csv")

    def add_schema(self, dataset: str):
        self.parser.add_argument("--raw_types", type=str, default=f"{self.root_dir}/{dataset}/raw/schemaorg-current-https-types.csv")

    def get_args(self, kb_name:str, model:str = None, template:int = None):
        """
            Return parser
        :return: parser
        """
        dataset, arguments = self.argument_getter.get(kb_name)
        
        # add dataset specific arguments
        arguments(dataset=dataset)
        self.parser.add_argument("--kb_name")
        self.parser.add_argument("--model")
        self.parser.add_argument("--device")
        
        # add general specific arguments
        self.parser.add_argument("--processed_hier", type=str, default=f"{self.root_dir}/{dataset}/processed/hierarchy_dict.json")
        self.parser.add_argument("--processed_train", type=str, default=f"{self.root_dir}/{dataset}/processed/hierarchy_train.json")
        self.parser.add_argument("--processed_test", type=str, default=f"{self.root_dir}/{dataset}/processed/hierarchy_test.json")
        self.parser.add_argument("--template_text", type=str, default=f"{self.root_dir}/templates.txt")
        self.parser.add_argument("--template", type=str, default=template)
        self.parser.add_argument("--labels_path", type=str, default=f"{self.root_dir}/label_mapper.json")
        self.parser.add_argument("--dataset", type=str, default=kb_name)
        self.parser.add_argument("--seed", type=int, default=555)
        self.parser.add_argument("--test_size", type=float, default=0.8)
        
        time = str(datetime.datetime.now()).split('.')[0]
        if model:
            self.mkdir(f"results/{kb_name}/{model}")
        self.parser.add_argument("--report_output", type=str, default=f"results/{kb_name}/{model}/report-{model}-{template}-{time}.json")
        # self.parser.add_argument("--model_output", type=str, default=f"results/{kb_name}/{model}/output-{model}-{template}-{time}.json")

        # add model specific arguments
        self.parser.add_argument("--batch_size", type=int, default=4)
        # add model specific arguments
        if model == "bert_large":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/bert-large-uncased")
            self.parser.add_argument("--model_name", type=str, default="bert")
        if model=="bart_large":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/bart-large")
            self.parser.add_argument("--model_name", type=str, default="bart")
        if model == "flan_t5_large":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/flan-t5-large")
            self.parser.add_argument("--model_name", type=str, default="t5")
        if model == "flan_t5_xl":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/flan-t5-xl")
            self.parser.add_argument("--model_name", type=str, default="t5")
        if model == "flan_t5_large_lm":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/flan-t5-large")
            self.parser.add_argument("--model_name", type=str, default="t5-lm")
        if model == "flan_t5_xl_lm":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/flan-t5-xl")
            self.parser.add_argument("--model_name", type=str, default="t5-lm")
        if model == "gpt2_large":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/gpt2-large")
            self.parser.add_argument("--model_name", type=str, default="gpt2")
        if model == "gpt2_xl":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/gpt2-xl")
            self.parser.add_argument("--model_name", type=str, default="gpt2")
        if model == "gpt3":
            self.parser.add_argument("--model_path", type=str, default="text-babbage-001")
            self.parser.add_argument("--model_name", type=str, default="gpt3")
            self.parser.add_argument("--model_output", type=str, default=f"results/{kb_name}/{model}/output-{model}-{template}-{time}.json")
        if model == "gpt4":
            self.parser.add_argument("--model_path", type=str, default="gpt-4-0613")
            self.parser.add_argument("--model_name", type=str, default="gpt4")
            self.parser.add_argument("--model_output", type=str, default=f"results/{kb_name}/{model}/output-{model}-{template}-{time}.json")
        if model == "gpt3_ada":
            self.parser.add_argument("--model_path", type=str, default="text-embedding-ada-002")
            self.parser.add_argument("--model_name", type=str, default="gpt3-ada")
            self.parser.add_argument("--model_output", type=str, default=f"results/{kb_name}/{model}/output-{model}-{template}-{time}.json")
        if model == "bloom_1b7":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/bloom-1b7")
            self.parser.add_argument("--model_name", type=str, default="bloom")
        if model == "bloom_3b":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/bloom-3b")
            self.parser.add_argument("--model_name", type=str, default="bloom")
        if model == "bloom_7b1":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/bloom-7b1")
            self.parser.add_argument("--model_name", type=str, default="bloom")
        if model == dataset.lower()+"_flan_t5_large":
            self.parser.add_argument("--model_path", type=str, default=f"../assets/FSL/{dataset.lower()}-flan-t5-large")
            self.parser.add_argument("--model_name", type=str, default="t5")
        if model == dataset.lower()+"_flan_t5_xl":
            self.parser.add_argument("--model_path", type=str, default=f"../assets/FSL/{dataset.lower()}-flan-t5-xl")
            self.parser.add_argument("--model_name", type=str, default="t5")
        self.parser.add_argument("-f")
        return self.parser.parse_args()


class ExternalEvaluationConfig:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def get_args(self):
        self.parser.add_argument("--root_dir", type=str, default="results")
        self.parser.add_argument("--kb_name", type=str, default="geonames")
        self.parser.add_argument("--model", type=str, default="gpt3")
        self.parser.add_argument("--template", type=str, default="template-1")
        self.parser.add_argument("--models_with_special_output", type=list, default=["gpt3", "gpt3_ada", "gpt4"])
        self.parser.add_argument("--label_mapper", type=str, default="../datasets/TaskB/label_mapper.json")
        self.parser.add_argument("-f")
        return self.parser.parse_args()