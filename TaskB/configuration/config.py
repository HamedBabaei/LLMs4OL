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
            "nci": ["NCI", self.add_umls],
            "snomedct_us": ["SNOMEDCT_US", self.add_umls],
            "medcin": ["MEDCIN", self.add_umls]
        }

    def add_geoname(self, dataset: str):
        self.parser.add_argument("--raw_feature_codes", type=str, default=f"dataset/{dataset}/raw/featureCodes_en.txt")
        self.parser.add_argument("--feature_codes", type=str, default=f"dataset/{dataset}/processed/feature_codes.csv")

    def add_umls(self, dataset: str):
        self.parser.add_argument("--raw_sn", type=str,
                                 default=f"dataset/{dataset}/raw/semantic_network.json")
        self.parser.add_argument("--processed_sn", type=str,
                                 default=f"dataset/{dataset}/processed/semantic_network.csv")

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
