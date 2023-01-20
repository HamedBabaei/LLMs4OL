"""
    DataConfig: Data Configuration of models
"""
import argparse


class BaseConfig:
    """
        Base Configs
    """
    def __init__(self, version: int= None):
        """
            Data configuration
        """
        self.parser = argparse.ArgumentParser()
        self.version = "" if version == None else "-" + str(version)
        self.argument_getter = {
            "wn18rr": self.add_wn18rr,  
            "geonames": self.add_geoname,
            "umls": self.add_umls
            }

    def add_wn18rr(self):
        dataset = "WN18RR"
        self.parser.add_argument("--raw_train", type=str, default=f"datasets/{dataset}/raw/train.txt")
        self.parser.add_argument("--raw_test", type=str, default=f"datasets/{dataset}/raw/test.txt")
        self.parser.add_argument("--raw_valid", type=str, default=f"datasets/{dataset}/raw/valid.txt")
        self.parser.add_argument("--definition", type=str, default="assets/WordNetDefinitions/wordnet-definitions.txt")
        self.parser.add_argument("--processed_train", type=str, default=f"datasets/{dataset}/processed{self.version}/train.csv")
        self.parser.add_argument("--processed_test", type=str, default=f"datasets/{dataset}/processed{self.version}/test.csv")
        self.parser.add_argument("--processed_valid", type=str, default=f"datasets/{dataset}/processed{self.version}/valid.csv")
        self.parser.add_argument("--processed_entity_train", type=str, default=f"datasets/{dataset}/processed{self.version}/entity_train.csv" )
        self.parser.add_argument("--processed_entity_test", type=str, default=f"datasets/{dataset}/processed{self.version}/entity_test.csv")
        self.parser.add_argument("--processed_entity_valid", type=str, default=f"datasets/{dataset}/processed{self.version}/entity_valid.csv")
        self.parser.add_argument("--relations_to_ignore", type=list, default=["_also_see"])
        
    def add_geoname(self):
        dataset = "Geonames"
        self.parser.add_argument("--feature_codes", type=str, default=f"datasets/{dataset}/raw/featureCodes_en.txt")
        self.parser.add_argument("--all_countries", type=str, default=f"datasets/{dataset}/raw/allCountries.txt")
        self.parser.add_argument("--depth", type=int, default=3)
        self.parser.add_argument("--processed_feature_codes", type=str, default=f"datasets/{dataset}/processed/featureCodes_en.csv")
        self.parser.add_argument("--processed_all_countries", type=str, default=f"datasets/{dataset}/processed/allCountries.csv")

    def add_umls(self):
        dataset = "UMLS"
        self.parser.add_argument("--tui2stn", type=str, default=f"datasets/{dataset}/processed/TUI2STN.json")
        self.parser.add_argument("--tui2str", type=str, default=f"datasets/{dataset}/processed/TUI2STR.json")
        self.parser.add_argument("--level1", type=str, default=f"datasets/{dataset}/processed/UMLS_STN_Hierarchy_level1.json")
        self.parser.add_argument("--level2", type=str, default=f"datasets/{dataset}/processed/UMLS_STN_Hierarchy_level2.json")
        self.parser.add_argument("--level3", type=str, default=f"datasets/{dataset}/processed/UMLS_STN_Hierarchy_level3.json")
        self.parser.add_argument("--umls_rel", type=str, default=f"datasets/{dataset}/processed/UMLS_skiped_bad_lines.tsv")
        self.parser.add_argument("--umls_entity", type=str, default=f"datasets/{dataset}/processed/UMLS_entity_types_with_levels.tsv")

    def get_args(self, db_name: str):
        """
            Return parser
        :return: parser
        """
        self.argument_getter.get(db_name)()
        self.parser.add_argument("-f")
        return self.parser.parse_args()
