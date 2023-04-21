from configs import BaseConfig
from datareader import DataReader
from datawriter import DataWriter
import random
from tqdm import tqdm
import os

def build_wn(config):
    dataset_json = DataReader.load_json(config.entity_path)
    label_mapper = DataReader.load_json(config.label_mapper)
    # pick N samples per class
    train_dataset = {}
    for key, label in label_mapper.items():
        train_dataset[key] = []
        for sample in dataset_json['train']:
            if sample['label'] == label and len(sample['sentence'].split()) > 3:
                train_dataset[key].append(sample)
            if len(train_dataset[key]) == config.n_per_class:
                break
    # checking the correctness of samples per class
    for key, val in train_dataset.items():
        assert len(train_dataset[key]) == config.n_per_class

    print("size of labels that has been considered:", len(train_dataset))
    custom_train_dataset = []
    for pos_label, positives in train_dataset.items():
        for positive in positives:
            custom_train_dataset.append({
                "negative": False,
                "yes-no-label": "yes",
                "[LABEL]": positive['label'],
                "[A]": positive['entity'],
                "[SENTENCE]": positive['sentence']
            })
            positive_label = positive['label']
        negatives_set = []
        for neg_label, negatives in train_dataset.items():
            if neg_label != pos_label:
                for negative in negatives:
                    negatives_set.append({
                        "[A]": negative['entity'],
                        "[SENTENCE]": negative['sentence']
                    })
        chosen_negatives = random.sample(negatives_set, config.neg_per_class)
        for chosen_negative in chosen_negatives:
            custom_train_dataset.append({
                "negative": True,
                "yes-no-label": "no",
                "[LABEL]": positive_label,
                "[A]": chosen_negative['[A]'],
                "[SENTENCE]": chosen_negative['[SENTENCE]']
            })
    # check if the  dataset builded correctly!
    assert len(custom_train_dataset) == len(label_mapper)*(config.n_per_class + config.neg_per_class)
    print("Size of final dataset is:", len(custom_train_dataset))
    return custom_train_dataset

def build_geonames(config):
    dataset_json = DataReader.load_json(config.entity_path)
    label_mapper = DataReader.load_json(config.label_mapper)
    modified_label_mapper = {label: content for label, content in label_mapper.items() if len(label) != 1}
    train_dataset = {}

    for key, label in tqdm(modified_label_mapper.items()):
        train_dataset[key] = []
        for sample in dataset_json['geonames']:
            if sample['type-label'] == key and sample['status'] == 'train':
                train_dataset[key].append(sample)
            if len(train_dataset[key]) == config.n_per_class:
                break

    # drom items that we dont have  data in train or less that config.n_per_class
    train_dataset = {key: items for key, items in train_dataset.items() if len(items) > 0}
    print("size of labels that has been considered:", len(train_dataset))

    custom_train_dataset = []
    for pos_label, positives in train_dataset.items():
        for positive in positives:
            custom_train_dataset.append({
                "negative": False,
                "yes-no-label": "yes",
                "type-label": positive['type-label'],
                "[LABEL]": positive['type-name'],
                "[NAME]": positive['name'],
                "[COUNTRY]": positive['country_name']
            })
        positive_type_label = positive['type-label']
        positive_name_label = positive['type-name']
        negatives_set = []
        for neg_label, negatives in train_dataset.items():
            if neg_label != pos_label:
                for negative in negatives:
                    negatives_set.append({
                        "[NAME]": negative['name'],
                        "[COUNTRY]": negative['country_name']
                    })
        chosen_negatives = random.sample(negatives_set, config.neg_per_class)
        for chosen_negative in chosen_negatives:
            custom_train_dataset.append({
                "negative": True,
                "yes-no-label": "no",
                "type-label": positive_type_label,
                "[LABEL]": positive_name_label,
                "[NAME]": chosen_negative['[NAME]'],
                "[COUNTRY]": chosen_negative['[COUNTRY]']
            })


    for index, sample in enumerate(custom_train_dataset):
        custom_train_dataset[index]['LABEL-SET'] = label_mapper[sample['type-label'][0]] + \
                                                    [label_mapper[sample['type-label']]['name']]+ \
                                                    label_mapper[sample['type-label']]['synonyms']
        custom_train_dataset[index]['LABEL-SET'] = list(set(custom_train_dataset[index]['LABEL-SET']))
    print("Size of final dataset is:", len(custom_train_dataset))
    return custom_train_dataset

def build_umls(config):
    dataset_json = DataReader.load_json(config.entity_path)
    label_mapper = DataReader.load_json(config.label_mapper)
    bio_rel = DataReader.load_json(os.path.join(config.biorel_dir, "test.json")) + \
              DataReader.load_json(os.path.join(config.biorel_dir, "dev.json")) + \
              DataReader.load_json(os.path.join(config.biorel_dir, "train.json"))
    bio_rel_cui_dict = {}
    for bio in bio_rel:
        bio_rel_cui_dict[bio['head']['CUI']] = {"word": bio['head']['word'], "sentence": bio['sentence']}
        bio_rel_cui_dict[bio['tail']['CUI']] = {"word": bio['tail']['word'], "sentence": bio['sentence']}

    train_dataset = {}
    for key, label in tqdm(label_mapper.items()):
        train_dataset[key] = []
        for sample in dataset_json:
            label_str_lst = eval(sample['label-str'])
            sentence = bio_rel_cui_dict.get(sample['cui'], "NONE")
            if len(train_dataset[key]) < config.n_per_class and sentence != "NONE":
                for type_label in label_str_lst:
                    if type_label == key and sample['status'] == 'train':
                        sample['sentence'] = sentence
                        sample['label-name'] = type_label
                        train_dataset[key].append(sample)
                    if len(train_dataset[key]) == config.n_per_class:
                        break
            if len(train_dataset[key]) == config.n_per_class:
                break
        if len(train_dataset[key]) < config.n_per_class:
            for sample in dataset_json:
                label_str_lst = eval(sample['label-str'])
                sentence = bio_rel_cui_dict.get(sample['cui'], "NONE")
                if len(train_dataset[key]) < config.n_per_class and sentence == "NONE":
                    for type_label in label_str_lst:
                        if type_label == key and sample['status'] == 'train':
                            sample['sentence'] = sentence
                            sample['label-name'] = type_label
                            train_dataset[key].append(sample)
                        if len(train_dataset[key]) == config.n_per_class:
                            break
                if len(train_dataset[key]) == config.n_per_class:
                    break
    # drom items that we dont have  data in train or less that config.n_per_class
    train_dataset = {key: items for key, items in train_dataset.items() if len(items) > 0}
    print("size of labels that has been considered:", len(train_dataset))

    custom_train_dataset = []
    for pos_label, positives in train_dataset.items():
        for positive in positives:
            if positive['sentence'] == "NONE":
                concept = positive['concept']
                is_contain_sentence = False
                sentence = concept
            else:
                concept = positive['sentence']['word']
                is_contain_sentence = True
                sentence = positive['sentence']['sentence']

            custom_train_dataset.append({
                "negative": False,
                "yes-no-label": "yes",
                "cui": positive['cui'],
                "type-label": positive['label-name'],
                "is_contain_sentence": is_contain_sentence,
                "[LABEL]": positive['label-names'],
                "[CONCEPT]": concept,
                "[SENTENCE]": sentence
            })
        positive_type_label = positive['label-name']
        positive_name_label = positive['label-names']
        negatives_set = []
        for neg_label, negatives in train_dataset.items():
            if neg_label != pos_label:
                for negative in negatives:
                    if negative['sentence'] == "NONE":
                        concept = negative['concept']
                        is_contain_sentence = False
                        sentence = concept
                    else:
                        concept = negative['sentence']['word']
                        is_contain_sentence = True
                        sentence = negative['sentence']['sentence']
                    negatives_set.append({
                        "cui": negative['cui'],
                        "is_contain_sentence": is_contain_sentence,
                        "[CONCEPT]": concept,
                        "[SENTENCE]": sentence
                    })
        chosen_negatives = random.sample(negatives_set, config.neg_per_class)
        for chosen_negative in chosen_negatives:
            custom_train_dataset.append({
                "negative": True,
                "yes-no-label": "no",
                "cui": chosen_negative['cui'],
                "type-label": positive_type_label,
                "is_contain_sentence": chosen_negative['is_contain_sentence'],
                "[LABEL]": positive_name_label,
                "[CONCEPT]": chosen_negative['[CONCEPT]'],
                "[SENTENCE]": chosen_negative['[SENTENCE]']
            })
    print("Size of final dataset is:", len(custom_train_dataset))
    for index, sample in enumerate(custom_train_dataset):
        custom_train_dataset[index]['LABEL-SET'] = label_mapper[sample['type-label']]
    return custom_train_dataset

if __name__=="__main__":
    config = BaseConfig(neg_per_class=3).get_args("wn18rr")
    custom_train_dataset = build_wn(config)
    DataWriter.write_json(custom_train_dataset, config.fsl_train_data)

    config = BaseConfig(neg_per_class=3).get_args("geonames")
    custom_train_dataset = build_geonames(config)
    DataWriter.write_json(custom_train_dataset, config.fsl_train_data)

    config = BaseConfig(neg_per_class=3).get_args("umls")
    custom_train_dataset = build_umls(config)
    DataWriter.write_json(custom_train_dataset, config.fsl_train_data)
