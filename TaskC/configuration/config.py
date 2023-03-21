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
            "umls":["UMLS", self.add_umls],
        }
        self.root_dir = "../datasets/TaskC"
        self.llms_root_dir = "../assets/LLMs"
        
    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def add_umls(self, dataset: str):
        self.parser.add_argument("--raw_sn", type=str, default=f"{self.root_dir}/{dataset}/raw/ ")
        self.parser.add_argument("--processed_sn", type=str, default=f"{self.root_dir}/{dataset}/processed/semantic_network.csv")

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
        # self.parser.add_argument("--processed_hier", type=str, default=f"{self.root_dir}/{dataset}/processed/hierarchy_dict.json")

        self.parser.add_argument("--template_text", type=str, default=f"{self.root_dir}/templates.txt")
        self.parser.add_argument("--template", type=str, default=template)
        self.parser.add_argument("--labels_path", type=str, default=f"{self.root_dir}/label_mapper.json")
        self.parser.add_argument("--dataset", type=str, default=kb_name)
        
        time = str(datetime.datetime.now()).split('.')[0]
        if model:
            self.mkdir(f"results/{kb_name}/{model}")
        self.parser.add_argument("--report_output", type=str, default=f"results/{kb_name}/{model}/report-{model}-{template}-{time}.json")

        # add model specific arguments
        self.parser.add_argument("--batch_size", type=int, default=1)
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
        
        self.parser.add_argument("-f")
        return self.parser.parse_args()