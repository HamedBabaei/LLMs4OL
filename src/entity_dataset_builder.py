from nltk.corpus import wordnet as wn
from collections import defaultdict

class EntityDatasetBuilder:

    def __init__(self, config, loader) -> None:
        self.config = config
        self.loader = loader
        self.dataset_dict = {}
        self.templates = None

    def build(self)-> dict:
        self.load_artifcats()
        return self.build_dataset()

    def load_artifcats(self):
        pass

    def build_dataset(self) -> dict:
        pass

    def build_train_set(self) -> dict:
        pass

    def build_test_set(self) -> dict:
        pass

    def build_stats(self) -> dict:
        pass

class WNEntityDatasetBuilder(EntityDatasetBuilder):

    def __init__(self, config, loader) -> None:
        super().__init__(config, loader)
        self.label_mapper = {"JJ":"adjective", "NN":"noun", "VB":"verb"}
        self.wn_types_identifier = {"J": wn.ADJ, "V":wn.VERB, "N": wn.NOUN}
        self.dataset_dict['label-mapper'] = self.label_mapper

    def load_artifcats(self):
        train, valid, test = self.loader.load_df(self.config.processed_entity_train), \
                             self.loader.load_df(self.config.processed_entity_valid), \
                             self.loader.load_df(self.config.processed_entity_test)
        self.train_entities = train.append(valid).reset_index(drop=True)['entity'].tolist()
        self.test_entities = test['entity'].tolist()
        self.templates = self.loader.load_json(self.config.templates_json)
        
    def build_dataset(self) -> dict:
        self.dataset_dict["templates"] = self.templates
        self.dataset_dict["train"] = self.build_train_set()
        self.dataset_dict["test"] = self.build_test_set()
        self.dataset_dict["stats"] = self.build_stats()
        return self.dataset_dict

    def make_sentence(self, concept: str, wn_type:str) -> str:
        sentence = concept
        synsets = wn.synsets("_".join(concept.split()), pos=self.wn_types_identifier[wn_type[0]])
        if len(synsets) != 0:
            example = synsets[0].examples()
            if len(example) != 0:
                sentence = example[0]
        return sentence

    def make_samples(self, entity:str) -> dict:
        concept, wn_type = " ".join(entity.split("_")[2:-2]), entity.split("_")[-2]
        label = self.label_mapper[wn_type]
        sentence = self.make_sentence(concept=concept, wn_type=wn_type)
        generated_templates = self.templates.copy()
        for key, template in generated_templates.items():
            if "[SENTENCE]" in template:
                template = template.replace("[SENTENCE]", sentence)
            template = template.replace("[A]", concept)
            generated_templates[key] = template
        return {
            "original-entity": entity,
            "entity": concept,
            "label": label,
            "generated-samples": generated_templates
        }

    def build_train_set(self):
        return  [self.make_samples(entity) 
                for entity in self.train_entities]
    
    def build_test_set(self):
        return [self.make_samples(entity) 
                for entity in self.test_entities]

    def build_stats(self) -> dict:
        def get_labels_freqs(data):
            freqs = defaultdict(int)
            for sample in data:
                freqs[sample['label']] += 1
            return freqs
        stats = {
            "# of labels": len(self.label_mapper),
            "train":{
                "# of samples": len(self.train_entities),
                "labels-freqs":  get_labels_freqs(self.dataset_dict["train"])
            },
            "test": {
                "# of samples": len(self.test_entities),
                "labels-freqs":  get_labels_freqs(self.dataset_dict["test"])
                }
        }
        return stats

class UMLSEntityDatasetBuilder(EntityDatasetBuilder):

    def __init__(self, config) -> None:
        super().__init__(config)

    def load_artifcats(self):
        pass

    def build_train_sample(self, entity):
        pass

    def build_test_sample(self, entity):
        pass

class GeonameEntityDatasetBuilder(EntityDatasetBuilder):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.levels_classes = {
            "level-1": ["A", "H", "L", "P", "R", "S", "T", "U", "V"],

            "level-3-A-ADM": {"ADM4":["ADM4", "ADM4H"], "ADM3":["ADM3", "ADM3H"], 
                              "ADM2":["ADM2", "ADM2H"], "ADM5":["ADM5", "ADM5H"], 
                              "ADMD":["ADMD", "ADMDH"], "ADM1":["ADM1", "ADM1H"]},

            "level-2-H": ["BAY", "CNL", "LK", "MRS", "PND", "RSV", "SPN", "STM", "WAD", "WLL"],
            "level-3-H-PND": {"PND":["PND"], "PNDI":["PNDI"]},
            "level-3-H-RSV": {"RSV":["RSV"], "RSVT":["RSVT"], "RSVI": ["RSVI"]},
            "level-3-H-STM": {"STM":["STM", "STMS"], "STMI":["STMI", "STMIX"],
                              "STMC":["STMC"], "STMD":["STMD", "STMQ"], 
                              "STMM":["STMM", "STMX", "STMH"], "STMB":["STMB", "STMA", "STMSB"]},

            "level-2-L":["ARE", "FLD", "GRA", "IND", "LCT", "OIL", "PRK", "RES", "RGN", "TRB"],
            "level-3-L-RES": {"RESF":["RESF", "RESP"], "RES":["RES"], "RESV":["RESV", "RESA"], 
                              "RESN":["RESN", "RESW"]},
                              
            "level-3-P-PPL": {"PPL":["PPL"], "PPLL":["PPLL", "PPLF"], "PPLQ":["PPLQ", "PPLW"],
                              "PPLX":["PPLX", "PPLH", "PPLCH", "PPLC", "PPLS", "PPLR", "PPLG"],
                              "PPLA":["PPLA", "PPLA2", "PPLA3", "PPLA4", "PPLA5"]},

            "level-2-R": ["FRM", "RD", "RDJ", "ST", "TNL"],

            "level-2-S": ["BLD", "CH", "CMT", "DAM", "FRM", "HMS", "HTL", "PO", "RST", "SCH", "TRL"],
            "level-3-S-FRM": {"FRMT":["FRMT", "FRMS"], "FRMQ":["FRMQ"]},
            "level-3-S-RST": {"RSTN": ["RSTN", "RSTNQ"], "RSTP":["RSTP", "RSTPQ"]},

            "level-2-T":["CAP", "HLL", "ISL", "MT", "MTS", "PAS", "PK", "PT", "RDG", "VAL"],
            "level-3-T-HLL": {"HLL":["HLL"], "HLLS":["HLLS"]},
            "level-3-T-ISL": {"ISL":["ISL"], "ISLET":["ISLET"], "ISLS":["ISLS"]},

            "level-2-V":["CUL", "FRS", "VIN"]
            }
    
    def load_artifcats(self):
        pass

    def build_train_sample(self, entity):
        pass

    def build_test_sample(self, entity):
        pass

class EntityDatasetBuilderFactory:

    def __init__(self, loader) -> None:
        self.builders = {
            "wn18rr": WNEntityDatasetBuilder,
            "umls": UMLSEntityDatasetBuilder,
            "geonames": GeonameEntityDatasetBuilder
        }
        self.loader = loader

    def __call__(self, config: str):
        return self.builders[config.dataset](config=config, loader=self.loader)
