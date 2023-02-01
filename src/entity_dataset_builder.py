from nltk.corpus import wordnet as wn
from collections import defaultdict
from tqdm import tqdm
from sklearn.model_selection import train_test_split


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
        self.wn_types_identifier = {"J": wn.ADJ, "V":wn.VERB, "N": wn.NOUN}
        

    def load_artifcats(self):
        train, valid, test = self.loader.load_df(self.config.processed_entity_train), \
                             self.loader.load_df(self.config.processed_entity_valid), \
                             self.loader.load_df(self.config.processed_entity_test)
        self.train_entities = train.append(valid).reset_index(drop=True)['entity'].tolist()
        self.test_entities = test['entity'].tolist()
        self.templates = self.loader.load_json(self.config.templates_json)
        self.label_mapper = self.loader.load_json(self.config.label_mapper)

    def build_dataset(self) -> dict:
        self.dataset_dict["templates"] = self.templates
        self.dataset_dict['label-mapper'] = self.label_mapper
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
        # generated_templates = self.templates.copy()
        # for key, template in generated_templates.items():
        #     if "[SENTENCE]" in template:
        #         template = template.replace("[SENTENCE]", sentence)
        #     template = template.replace("[A]", concept)
        #     generated_templates[key] = template
        return {
            "original-entity": entity,
            "entity": concept,
            "label": label,
            "sentence": sentence
            # "generated-samples": generated_templates
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
    def __init__(self, config, loader) -> None:
        super().__init__(config, loader)
    
    def load_artifcats(self):
        self.heirarchy = self.loader.load_json(self.config.heirarchy)
        self.templates = self.loader.load_json(self.config.templates_json)
        self.label_mapper = self.loader.load_json(self.config.label_mapper)
        self.countries_df  = self.loader.load_df(self.config.processed_all_countries)
        # feature_codes  = self.loader.load_df(self.config.processed_feature_codes)
        countrycode_names_js = self.loader.load_json(self.config.countrycode_names_json)
        self.countrycode_names_mapper = {cc_names['Code']: cc_names['Name'] for cc_names in countrycode_names_js}

    def build_dataset(self) -> dict:
        geoname = self.make_dataset_dict()
        geoname = self.create_train_test_in_levels(geoname)
        self.dataset_dict["templates"] = self.templates
        self.dataset_dict['label-mapper'] = self.label_mapper
        self.dataset_dict['heirarchy'] = self.heirarchy
        self.dataset_dict['geonames'] = self.make_samples(geoname)
        self.dataset_dict["stats"] = self.build_stats()
        return self.dataset_dict
        
    def make_dataset_dict(self) -> list[dict]:
        geoname = []
        for index, name, asciiname, country_code, level1, level2, level3 in tqdm(zip(range(0,self.countries_df.shape[0]),
                                                                                             self.countries_df['name'].tolist(),
                                                                                             self.countries_df['asciiname'].tolist(),
                                                                                             self.countries_df['country-code'].tolist(),
                                                                                             self.countries_df['level-1'].tolist(),
                                                                                             self.countries_df['level-2'].tolist(),
                                                                                             self.countries_df['level-3'].tolist())):
            if str(country_code) == "nan":
                country_code = "not identified country"
            country_name = self.countrycode_names_mapper.get(country_code, country_code)
            geoname.append({
                "index": index,
                "name": name,
                "asciname": asciiname,
                "country_code": country_code,
                "country_name": country_name,
                "level1": level1,
                "level2": level2,
                "level3": level3,
            })
        return geoname
    
    def create_train_test_in_levels(self, geoname: list[dict]) -> list[dict]:
        for level, classes in tqdm(self.heirarchy.items()):
            if level.startswith("level-1"):
                geoname = self.create_train_test_in_level_x(geoname=geoname, classes=classes, label_key="level1", branch=level)
            elif level.startswith("level-2"):
                geoname = self.create_train_test_in_level_x(geoname=geoname, classes=classes, label_key="level2", branch=level)
            else:
                geoname = self.create_train_test_in_level_3(geoname=geoname, classes=classes, label_key="level3", branch=level)
        return geoname

    def create_train_test_in_level_x(self, geoname: list[dict], classes: list, label_key: str, branch: str) -> list[dict]:
        indexes, labels = [], []
        for geo in geoname:
            if geo[label_key] in classes:
                indexes.append(geo['index'])
                labels.append(geo[label_key])
        train_indexes, test_indexes, _, _ = train_test_split(indexes, labels, 
                                                             test_size=self.config.test_size,
                                                             random_state=self.config.seed)
        train_indexes_dict = {index:"OK" for index in train_indexes}
        test_indexes_dict = {index:"OK" for index in test_indexes}
        for index, geo in enumerate(geoname):
            if train_indexes_dict.get(geo['index'], "NOT_OK") == "OK":
                geoname[index]["status-in-"+branch] = "train"
                geoname[index]["label-in-"+branch] = geo[label_key]
                geoname[index]["label-strings-in-"+branch] = self.label_mapper[geo[label_key]]

            elif test_indexes_dict.get(geo['index'], "NOT_OK") == "OK":
                geoname[index]["status-in-"+branch] = "test"
                geoname[index]["label-in-"+branch] = geo[label_key]
                geoname[index]["label-strings-in-"+branch] = self.label_mapper[geo[label_key]]
        return geoname    

    def create_train_test_in_level_3(self, geoname: list[dict], classes: dict, label_key: str, branch: str) -> list[dict]:
        indexes, labels = [], []
        classes_dict = {}
        for key, items in classes.items():
            for item in items:
                classes_dict[item] = key
        for geo in geoname:
            if geo[label_key] in list(classes_dict.keys()):
                indexes.append(geo['index'])
                labels.append(classes_dict[geo[label_key]])

        train_indexes, test_indexes, _, _ = train_test_split(indexes, labels, 
                                                            test_size=self.config.test_size,
                                                            random_state=self.config.seed)
        train_indexes_dict = {index:"OK" for index in train_indexes}
        test_indexes_dict = {index:"OK" for index in test_indexes}
        for index, geo in enumerate(geoname):
            if train_indexes_dict.get(geo['index'], "NOT_OK") == "OK":
                geoname[index]["status-in-"+branch] = "train"
                geoname[index]["label-in-"+branch] = classes_dict[geo[label_key]]
                geoname[index]["label-strings-in-"+branch] = self.label_mapper[classes_dict[geo[label_key]]]
            elif test_indexes_dict.get(geo['index'], "NOT_OK") == "OK":
                geoname[index]["status-in-"+branch] = "test"
                geoname[index]["label-in-"+branch] = classes_dict[geo[label_key]]
                geoname[index]["label-strings-in-"+branch] = self.label_mapper[classes_dict[geo[label_key]]]
        return geoname    

    def make_samples(self, geoname:list[dict]) -> list[dict]:
        # def generate_samples(country:str, name:str) -> dict:
        #     generated_templates = self.templates.copy()
        #     for key, template in generated_templates.items():
        #         if "[COUNTRY]" in template:
        #             template = template.replace("[COUNTRY]", country)
        #         template = template.replace("[A]", name)
        #         generated_templates[key] = template
        #     return generated_templates
        # for index, geo in tqdm(enumerate(geoname)):
        #     geoname[index]['generated-samples'] = generate_samples(country=geo['country_name'], name=str(geo['asciname']))
        return geoname
    
    def build_stats(self) -> dict:
        def get_labels_freqs(label_in_branch, status_in_branch, status):
            freqs = defaultdict(int)
            samples_no = 0
            for sample in self.dataset_dict['geonames']:
                if label_in_branch in list(sample.keys()):
                    if sample[status_in_branch] == status:
                        freqs[sample[label_in_branch]] += 1
                        samples_no += 1
            return freqs, samples_no
        stats = {
            "# of labels at all": len(self.label_mapper),
            "# of samples at all": len(self.dataset_dict['geonames']),
        }
        for branch, classes in self.heirarchy.items():
            train_stats, train_size = get_labels_freqs(label_in_branch = "label-in-"+branch, status_in_branch="status-in-"+branch, status="train")
            test_stats, test_size = get_labels_freqs(label_in_branch = "label-in-"+branch, status_in_branch="status-in-"+branch, status="test")
            stats[branch] = {
                "# of labels": len(classes), 
                "# of train samples": train_size,
                "# of test samples": test_size,
                "labels-freqs in train": train_stats,
                "labels-freqs in test": test_stats,
                }
        return stats


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
