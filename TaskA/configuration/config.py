"""
    BaseConfig: Data Configuration of models
"""
import argparse
import datetime
import os
import torch

class BaseConfig:
    """
        Base Configs
    """
    def __init__(self, version: int= None):
        """
            Data configuration
        """
        self.root_dir = "../datasets/TaskA"
        self.llms_root_dir = "../assets/LLMs"
        self.parser = argparse.ArgumentParser()
        self.version = "" if version == None else "-" + str(version)
        self.argument_getter = {
            "wn18rr": ["WN18RR", self.add_wn18rr],
            "geonames": ["Geonames", self.add_geoname],
            "umls": ["UMLS", self.add_umls],
            "nci": ["UMLS", self.add_umls],
            "snomedct_us": ["UMLS", self.add_umls],
            "medcin": ["UMLS", self.add_umls]
            }

        self.answer_set_generator_domains_getter = {
            "wn18rr": "lexicosemantics",
            "geonames": "geography",
            "umls": "medicine"
        }

    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def add_wn18rr(self, dataset: str):
        self.parser.add_argument("--raw_train", type=str, default=f"{self.root_dir}/{dataset}/raw/train.txt")
        self.parser.add_argument("--raw_test", type=str, default=f"{self.root_dir}/{dataset}/raw/test.txt")
        self.parser.add_argument("--raw_valid", type=str, default=f"{self.root_dir}/{dataset}/raw/valid.txt")
        self.parser.add_argument("--definition", type=str, default="../assets/WordNetDefinitions/wordnet-definitions.txt")
        self.parser.add_argument("--processed_train", type=str, default=f"{self.root_dir}/{dataset}/processed{self.version}/train.csv")
        self.parser.add_argument("--processed_test", type=str, default=f"{self.root_dir}/{dataset}/processed{self.version}/test.csv")
        self.parser.add_argument("--processed_valid", type=str, default=f"{self.root_dir}/{dataset}/processed{self.version}/valid.csv")
        self.parser.add_argument("--processed_entity_train", type=str, default=f"{self.root_dir}/{dataset}/processed{self.version}/entity_train.csv" )
        self.parser.add_argument("--processed_entity_test", type=str, default=f"{self.root_dir}/{dataset}/processed{self.version}/entity_test.csv")
        self.parser.add_argument("--processed_entity_valid", type=str, default=f"{self.root_dir}/{dataset}/processed{self.version}/entity_valid.csv")
        self.parser.add_argument("--relations_to_ignore", type=list, default=["_also_see", "_member_of_domain_region",  
                                                                              "_similar_to", "_member_of_domain_usage"])
        self.parser.add_argument("--entity_class_to_ignore", type=list, default=["RB"])
        
        
    def add_geoname(self, dataset: str):
        self.parser.add_argument("--feature_codes", type=str, default=f"{self.root_dir}/{dataset}/raw/featureCodes_en.txt")
        self.parser.add_argument("--all_countries", type=str, default=f"{self.root_dir}/{dataset}/raw/allCountries.txt")
        self.parser.add_argument("--depth", type=int, default=3)
        self.parser.add_argument("--processed_feature_codes", type=str, default=f"{self.root_dir}/{dataset}/processed{self.version}/featureCodes_en.csv")
        self.parser.add_argument("--processed_all_countries", type=str, default=f"{self.root_dir}/{dataset}/processed{self.version}/allCountries.csv")
        self.parser.add_argument("--countrycode_names_csv", type=str, default=f"../assets/CountryCodes/country_codes.csv")
        self.parser.add_argument("--countrycode_names_json", type=str, default=f"../assets/CountryCodes/country_codes.json")

    def add_umls(self, dataset: str):
        self.parser.add_argument("--tui2stn", type=str, default=f"{self.root_dir}/{dataset}/processed/TUI2STN.json")
        self.parser.add_argument("--tui2str", type=str, default=f"{self.root_dir}/{dataset}/processed/TUI2STR.json")
        self.parser.add_argument("--level1", type=str, default=f"{self.root_dir}/{dataset}/processed/UMLS_STN_Hierarchy_level1.json")
        self.parser.add_argument("--level2", type=str, default=f"{self.root_dir}/{dataset}/processed/UMLS_STN_Hierarchy_level2.json")
        self.parser.add_argument("--level3", type=str, default=f"{self.root_dir}/{dataset}/processed/UMLS_STN_Hierarchy_level3.json")
        self.parser.add_argument("--level4", type=str, default=f"{self.root_dir}/{dataset}/processed/UMLS_STN_Hierarchy_level4.json")
        self.parser.add_argument("--raw_umls_rel", type=str, default=f"{self.root_dir}/{dataset}/processed-3/UMLS_feb_skiped_bad_lines.tsv")
        self.parser.add_argument("--raw_umls_entity", type=str, default=f"{self.root_dir}/{dataset}/processed/UMLS_entity_types_with_levels.tsv")
        self.parser.add_argument("--umls_processed_dir", type=str, default=f"{self.root_dir}/{dataset}/processed{self.version}")
        self.parser.add_argument("--sources_to_consider", type=list, default=["NCI", "SNOMEDCT_US", "MEDCIN"])

    def get_args(self, kb_name:str, model:str = None, template:str = None):
        """
            Return parser
        :return: parser
        """
        dataset, arguments = self.argument_getter.get(kb_name) 

        # add dataset specific arguments
        arguments(dataset=dataset)
        self.parser.add_argument("--kb_name")
        self.parser.add_argument("--model_name")
        self.parser.add_argument("--device")
        # add general specific arguments
        self.parser.add_argument("--dataset", type=str, default=kb_name)
        time = str(datetime.datetime.now()).split('.')[0]
        if dataset == "UMLS" and kb_name != "umls":
            print("working with entity path of:", f"datasets/TaskA/{dataset}/{kb_name}_entities.json")
            self.parser.add_argument("--entity_path", type=str, default=f"{self.root_dir}/{dataset}/{kb_name}_entities.json")
            self.parser.add_argument("--dataset_stats", type=str, default=f"{self.root_dir}/{dataset}/{kb_name}_stats.json")
        else:
            self.parser.add_argument("--entity_path", type=str, default=f"{self.root_dir}/{dataset}/{dataset.lower()}_entities.json")
            self.parser.add_argument("--dataset_stats", type=str, default=f"{self.root_dir}/{dataset}/stats.json")
        if model:
            self.mkdir(f"results/{kb_name}/{model}")
        self.parser.add_argument("--report_output", type=str, default=f"results/{kb_name}/{model}/report-{model}-{template}-{time}.json")
        if model == "gpt3":
            self.parser.add_argument("--model_output", type=str, default=f"results/{kb_name}/{model}/output-{model}-{template}-batch [BATCH]-{time}.json")
        else:
            self.parser.add_argument("--model_output", type=str, default=f"results/{kb_name}/{model}/output-{model}-{template}-{time}.json")

        self.parser.add_argument("--templates_json", type=str, default=f"{self.root_dir}/{dataset}/templates.json")
        self.parser.add_argument("--label_mapper", type=str, default=f"{self.root_dir}/{dataset}/label_mapper.json")
        self.parser.add_argument("--chatgpt_label_mapper", type=str, default=f"{self.root_dir}/{dataset}/chatgpt_label_mapper.json")
        self.parser.add_argument("--answer_set_generator_n", type=int, default=10)
        self.parser.add_argument("--answer_set_generator_domains", type=str, default=self.answer_set_generator_domains_getter.get(kb_name, "NAN"))

        self.parser.add_argument("--heirarchy", type=str, default=f"{self.root_dir}/{dataset}/heirarchy.json")
        self.parser.add_argument("--test_size", type=float, default=0.08)  # This is for UMLS and Geoname Levels!
        self.parser.add_argument("--seed", type=int, default=555)


        self.parser.add_argument("--template", type=str, default=template)
        self.parser.add_argument("--top_n", type=int, default=1)
        self.parser.add_argument("--eval_ks", type=list, default=[1, 5, 10])
        self.parser.add_argument("--eval_metric", type=str, default="map")
        if model == "gpt3":
            self.parser.add_argument("--batch_size", type=int, default=10000)
        elif model == "gpt4":
            self.parser.add_argument("--batch_size", type=int, default=10000)
        else:
            self.parser.add_argument("--batch_size", type=int, default=16)
        # add model specific arguments
        if model == "bert_large":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/bert-large-uncased")
            self.parser.add_argument("--template_name", type=str, default="bert")
            self.parser.add_argument("--multi_gpu", type=bool, default=False)
        if model=="bart_large":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/bart-large")
            self.parser.add_argument("--template_name", type=str, default="bart")
            self.parser.add_argument("--multi_gpu", type=bool, default=False)
        if model == "flan_t5_large":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/flan-t5-large")
            self.parser.add_argument("--template_name", type=str, default="t5")
            self.parser.add_argument("--multi_gpu", type=bool, default=True)
        if model == "flan_t5_xl":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/flan-t5-xl")
            self.parser.add_argument("--template_name", type=str, default="t5")
            self.parser.add_argument("--multi_gpu", type=bool, default=True)
        if model == "gpt3":
            self.parser.add_argument("--model_path", type=str, default="text-babbage-001")
            self.parser.add_argument("--template_name", type=str, default="gpt3")
            self.parser.add_argument("--gpt3_max_tokens", type=int, default=10)
            self.parser.add_argument("--multi_gpu", type=bool, default=False)
        if model == "gpt4":
            self.parser.add_argument("--model_path", type=str, default="gpt-4-0613")
            self.parser.add_argument("--template_name", type=str, default="gpt3")
            self.parser.add_argument("--gpt4_max_tokens", type=int, default=10)
            self.parser.add_argument("--multi_gpu", type=bool, default=False)
        if model == "chatgpt":
            self.parser.add_argument("--model_path", type=str, default="gpt-3.5-turbo-0613")
            self.parser.add_argument("--template_name", type=str, default="gpt3")
            self.parser.add_argument("--chatgpt_max_tokens", type=int, default=10)
            self.parser.add_argument("--multi_gpu", type=bool, default=False)
        if model == "bloom_1b7":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/bloom-1b7")
            self.parser.add_argument("--template_name", type=str, default="bloom")
            self.parser.add_argument("--multi_gpu", type=bool, default=False)
        if model == "bloom_3b":
            self.parser.add_argument("--model_path", type=str, default=f"{self.llms_root_dir}/bloom-3b")
            self.parser.add_argument("--template_name", type=str, default="bloom")
            self.parser.add_argument("--multi_gpu", type=bool, default=False)
        if model == "llama_7b":
            self.parser.add_argument("--model_path", type=str, default="huggyllama/llama-7b")
            self.parser.add_argument("--template_name", type=str, default="gpt3")
            self.parser.add_argument("--multi_gpu", type=bool, default=False)
        if model == dataset.lower()+"_flan_t5_large":
            self.parser.add_argument("--model_path", type=str, default=f"../assets/FSL/{dataset.lower()}-flan-t5-large")
            self.parser.add_argument("--template_name", type=str, default="t5")
            self.parser.add_argument("--multi_gpu", type=bool, default=False)
        if model == dataset.lower()+"_flan_t5_xl":
            self.parser.add_argument("--model_path", type=str, default=f"../assets/FSL/{dataset.lower()}-flan-t5-xl")
            self.parser.add_argument("--template_name", type=str, default="t5")
            self.parser.add_argument("--multi_gpu", type=bool, default=False)
        # for multi-gpu only
        self.parser.add_argument("--gpu_no", type=int, default=torch.cuda.device_count())
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
        self.parser.add_argument("--models_with_special_output", type=list, default=["gpt3", "gpt4"])
        self.parser.add_argument("--eval_ks", type=list, default=[1, 5, 10])
        self.parser.add_argument("--eval_metric", type=str, default="map")
        self.parser.add_argument("-f")
        return self.parser.parse_args()