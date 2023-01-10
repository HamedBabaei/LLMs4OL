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

        
    def add_wnn18rr(self):
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
        
    def add_fb15k_237(self):
        dataset = "FB15K-237"
        self.parser.add_argument("--raw_train", type=str, default=f"datasets/{dataset}/raw/train.txt")
        self.parser.add_argument("--raw_test", type=str, default=f"datasets/{dataset}/raw/test.txt")
        self.parser.add_argument("--raw_valid", type=str, default=f"datasets/{dataset}/raw/valid.txt")
        self.parser.add_argument("--freebase_dumps_dir", type=str, default=f"assets/FreeBase/FreeBase_FB15KBased_Dumps")
        self.parser.add_argument("--freebase_hierarchy", type=str, default=f"assets/FreeBase/freebase_llms2ol_hierarchy.json")
        self.parser.add_argument("--freebase_types", type=str, default=f"assets/FreeBase/freebaseTypes.tsv")
        
        
        self.parser.add_argument("--processed_train_rel", type=str, default=f"datasets/{dataset}/processed{self.version}/train_rel.csv")
        self.parser.add_argument("--processed_test_rel", type=str, default=f"datasets/{dataset}/processed{self.version}/test_rel.csv")
        self.parser.add_argument("--processed_valid_rel", type=str, default=f"datasets/{dataset}/processed{self.version}/valid_rel.csv")

        self.parser.add_argument("--processed_train_ent", type=str, default=f"datasets/{dataset}/processed{self.version}/train_ent.csv")
        self.parser.add_argument("--processed_test_ent", type=str, default=f"datasets/{dataset}/processed{self.version}/test_ent.csv")
        self.parser.add_argument("--processed_valid_ent", type=str, default=f"datasets/{dataset}/processed{self.version}/valid_ent.csv")

        self.parser.add_argument("--processed_wordnet_taxonomy", type=str, 
                                    default=f"datasets/{dataset}/processed{self.version}/processed_wordnet_taxonomy.csv")

    def add_geoname(self):
        dataset = "Geonames"
        self.parser.add_argument("--feature_codes", type=str, default=f"datasets/{dataset}/raw/featureCodes_en.txt")
        self.parser.add_argument("--all_countries", type=str, default=f"datasets/{dataset}/raw/allCountries.txt")
        self.parser.add_argument("--depth", type=int, default=3)

        self.parser.add_argument("--processed_feature_codes", type=str, default=f"datasets/{dataset}/processed/featureCodes_en.csv")
        self.parser.add_argument("--processed_all_countries", type=str, default=f"datasets/{dataset}/processed/allCountries.csv")

    def get_args(self, db_name: str):
        """
            Return parser
        :return: parser
        """
        if db_name == "wn18rr":
            self.add_wnn18rr()
        if db_name == "fb15k-237":
            self.add_fb15k_237()
        if db_name == "geonames":
            self.add_geoname()
        self.parser.add_argument("-f")
        return self.parser.parse_args()
