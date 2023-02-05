"""
    DataConfig: Data Configuration of models
"""
import argparse
import datetime

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
            "wn18rr": ["WN18RR", self.add_wn18rr],
            "geonames": ["Geonames", self.add_geoname],
            "umls": ["UMLS", self.add_umls],
            "nci": ["UMLS", self.add_umls],
            "snomedct_us": ["UMLS", self.add_umls],
            "medicin": ["UMLS", self.add_umls]
            }

    def add_wn18rr(self, dataset: str):
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
        self.parser.add_argument("--relations_to_ignore", type=list, default=["_also_see", "_member_of_domain_region",  
                                                                              "_similar_to", "_member_of_domain_usage"])
        self.parser.add_argument("--entity_class_to_ignore", type=list, default=["RB"])
        
        
    def add_geoname(self, dataset: str):
        self.parser.add_argument("--feature_codes", type=str, default=f"datasets/{dataset}/raw/featureCodes_en.txt")
        self.parser.add_argument("--all_countries", type=str, default=f"datasets/{dataset}/raw/allCountries.txt")
        self.parser.add_argument("--depth", type=int, default=3)
        self.parser.add_argument("--processed_feature_codes", type=str, default=f"datasets/{dataset}/processed{self.version}/featureCodes_en.csv")
        self.parser.add_argument("--processed_all_countries", type=str, default=f"datasets/{dataset}/processed{self.version}/allCountries.csv")
        self.parser.add_argument("--countrycode_names_csv", type=str, default=f"assets/CountryCodes/country_codes.csv")
        self.parser.add_argument("--countrycode_names_json", type=str, default=f"assets/CountryCodes/country_codes.json")

    def add_umls(self, dataset: str):
        self.parser.add_argument("--tui2stn", type=str, default=f"datasets/{dataset}/processed/TUI2STN.json")
        self.parser.add_argument("--tui2str", type=str, default=f"datasets/{dataset}/processed/TUI2STR.json")
        self.parser.add_argument("--level1", type=str, default=f"datasets/{dataset}/processed/UMLS_STN_Hierarchy_level1.json")
        self.parser.add_argument("--level2", type=str, default=f"datasets/{dataset}/processed/UMLS_STN_Hierarchy_level2.json")
        self.parser.add_argument("--level3", type=str, default=f"datasets/{dataset}/processed/UMLS_STN_Hierarchy_level3.json")
        self.parser.add_argument("--level4", type=str, default=f"datasets/{dataset}/processed/UMLS_STN_Hierarchy_level4.json")
        self.parser.add_argument("--raw_umls_rel", type=str, default=f"datasets/{dataset}/processed/UMLS_skiped_bad_lines.tsv")
        self.parser.add_argument("--raw_umls_entity", type=str, default=f"datasets/{dataset}/processed/UMLS_entity_types_with_levels.tsv")
        self.parser.add_argument("--umls_processed_dir", type=str, default=f"datasets/{dataset}/processed{self.version}")
        self.parser.add_argument("--sources_to_consider", type=list, default=["NCI", "SNOMEDCT_US", "MEDICIN"])


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
        # add general specific arguments
        self.parser.add_argument("--dataset", type=str, default=kb_name)
        time = str(datetime.datetime.now()).split('.')[0]
        if dataset == "UMLS" and kb_name != "umls":
            print("working with entity path of:", f"datasets/{dataset}/{kb_name}_entities.json")
            self.parser.add_argument("--entity_path", type=str, default=f"datasets/{dataset}/{kb_name}_entities.json")
            self.parser.add_argument("--report_output", type=str, default=f"results/{dataset}/{kb_name}-report-{model}-{template}-{time}.json")
            self.parser.add_argument("--model_output", type=str, default=f"results/{dataset}/{kb_name}-output-{model}-{template}-{time}.json")
        else:
            self.parser.add_argument("--entity_path", type=str, default=f"datasets/{dataset}/{dataset.lower()}_entities.json")
            self.parser.add_argument("--report_output", type=str, default=f"results/{dataset}/report-{model}-{template}-{time}.json")
            self.parser.add_argument("--model_output", type=str, default=f"results/{dataset}/output-{model}-{template}-{time}.json")

        self.parser.add_argument("--templates_json", type=str, default=f"datasets/{dataset}/templates.json")
        self.parser.add_argument("--label_mapper", type=str, default=f"datasets/{dataset}/label_mapper.json")
        self.parser.add_argument("--heirarchy", type=str, default=f"datasets/{dataset}/heirarchy.json")
        self.parser.add_argument("--test_size", type=float, default=0.20)  # This is for UMLS and Geoname Levels!
        self.parser.add_argument("--seed", type=int, default=555)
        
        # add model specific arguments
        if model=="bert_large":
            self.parser.add_argument("--model_path", type=str, default="bert-large-uncased")
            self.parser.add_argument("--batch_size", type=int, default=64)
            self.parser.add_argument("--top_n", type=int, default=10)
            self.parser.add_argument("--device", type=str, default="cpu")
            self.parser.add_argument("--template", type=str, default=template)
            
        if model=="ngram":
            self.parser.add_argument("--top_n", type=int, default=10)

        self.parser.add_argument("-f")
        return self.parser.parse_args()
