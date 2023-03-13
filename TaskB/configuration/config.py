"""
    DataConfig: Data Configuration of models
"""
import argparse
import datetime

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
            "umls":["UMLS", self.add_umls]
        }
        self.root_dir = "../datasets/TaskB"

    def add_geoname(self, dataset: str):
        self.parser.add_argument("--raw_feature_codes", type=str, default=f"{self.root_dir}/{dataset}/raw/featureCodes_en.txt")
        self.parser.add_argument("--feature_codes", type=str, default=f"{self.root_dir}/{dataset}/processed/feature_codes.csv")
        self.parser.add_argument("--processed_hier", type=str, default=f"{self.root_dir}/{dataset}/processed/hierarchy_dict.json")

    def add_umls(self, dataset: str):
        self.parser.add_argument("--raw_sn_nci", type=str, default=f"{self.root_dir}/{dataset}/raw/nci_semantic_network.json")
        self.parser.add_argument("--raw_sn_medcin", type=str, default=f"{self.root_dir}/{dataset}/raw/medcin_semantic_network.json")
        self.parser.add_argument("--raw_sn_snomedct_us", type=str, default=f"{self.root_dir}/{dataset}/raw/snomedct_us_semantic_network.json")
        self.parser.add_argument("--raw_sn", type=str, default=f"{self.root_dir}/{dataset}/raw/semantic_network.json")
        self.parser.add_argument("--processed_sn", type=str, default=f"{self.root_dir}/{dataset}/processed/semantic_network.csv")
        self.parser.add_argument("--processed_hier", type=str, default=f"{self.root_dir}/{dataset}/processed/hierarchy_dict.json")

    def get_args(self, kb_name:str):
        """
            Return parser
        :return: parser
        """
        dataset, arguments = self.argument_getter.get(kb_name)
        # add dataset specific arguments
        arguments(dataset=dataset)
        self.parser.add_argument("-f")
        return self.parser.parse_args()
