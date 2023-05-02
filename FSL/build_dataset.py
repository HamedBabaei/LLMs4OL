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

    # drom items that we don't have  data in train or less that config.n_per_class
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
                "[NAME]": positive['asciname'],
                "[COUNTRY]": positive['country_name']
            })
        positive_type_label = positive['type-label']
        positive_name_label = positive['type-name']
        negatives_set = []
        for neg_label, negatives in train_dataset.items():
            if neg_label != pos_label:
                for negative in negatives:
                    negatives_set.append({
                        "[NAME]": negative['asciname'],
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


def add_task_b_info_geonames(config, dataset_json):
    def get_searchable_class(triple):
        if len(triple[0]) == 1 and len(triple[1]) != 1:
            return triple[1]
        if len(triple[1]) == 1 and len(triple[0]) != 1:
            return triple[0]
        return "NA"

    label_mapper = DataReader.load_json(config.label_mapper)
    task_b = DataReader.load_json(config.geonames_task_b_train)
    task_b_new = []
    for item in task_b:
        text_a_label, text_b_label = "", ""
        label = 'yes' if item['label'] == 'correct' else 'no'
        for key, word_sets in label_mapper.items():
            if len(key) == 1:
                for word in word_sets:
                    if word in item['text_b']:
                        text_b_label = key
                    elif word in item['text_a']:
                        text_a_label = key
            elif word_sets['name'] == item['text_b']:
                text_b_label = key
            elif word_sets['name'] == item['text_a']:
                text_a_label = key
            if text_a_label != "" and text_b_label != "":
                break
        task_b_new.append({"label-triples": [text_a_label, text_b_label, label], "label-names": item, "used": False})

    data_labels = set([data['type-label'] for data in dataset_json])
    task_b_labels = set([label for data in task_b_new for label in data['label-triples']])
    intersect = data_labels.intersection(task_b_labels)
    print("dataset types:", len(data_labels))
    print("Task_b train set types:", len(task_b_labels))
    print("intersection:", len(intersect))

    for data in dataset_json:
        data['task-b'] = False
    for task_b_data in task_b_new:
        search_type = get_searchable_class(task_b_data['label-triples'])
        for index, data in enumerate(dataset_json):
            if not data['task-b'] and search_type != 'NA' and not data['negative']:
                if data['type-label'] == search_type:
                    dataset_json[index]['task-b'] = True
                    dataset_json[index]['task-b-items'] = task_b_data['label-names']
    return dataset_json


def add_task_b_info_umls(config, dataset_json):
    label_mapper = DataReader.load_json(config.label_mapper)
    task_b = DataReader.load_json(config.umls_task_b_train)
    task_b_new = []
    for item in task_b:
        text_a_label, text_b_label = "", ""
        label = 'yes' if item['label'] == 'correct' else 'no'
        for key, word_sets in label_mapper.items():
            word_sets_lower = [word.lower() for word in word_sets]
            if item['text_b'] in word_sets_lower:
                text_b_label = key
            elif item['text_a'] in word_sets_lower:
                text_a_label = key
            if text_a_label != "" and text_b_label != "":
                break
        if text_a_label != "" and text_b_label != "":
            task_b_new.append({"label-triples": [text_a_label, text_b_label, label], "label-names": item, "used": False})

    data_labels = set([data['type-label'] for data in dataset_json])
    task_b_labels = set([label for data in task_b_new for label in data['label-triples']])
    intersect = data_labels.intersection(task_b_labels)
    print("dataset types:", len(data_labels))
    print("Task_b train set types:", len(task_b_labels))
    print("intersection:", len(intersect))

    for data in dataset_json:
        data['task-b'] = False
    for task_b_data in task_b_new:
        search_type_a, search_type_b = task_b_data['label-triples'][0], task_b_data['label-triples'][1]
        for index, data in enumerate(dataset_json):
            if not data['task-b'] and not data['negative']:
                if search_type_a == data['type-label'] or search_type_b == data['type-label']:
                    dataset_json[index]['task-b'] = True
                    dataset_json[index]['task-b-items'] = task_b_data['label-names']
    return dataset_json

def add_task_c_info_umls(config, dataset_json):
    label_mapper = DataReader.load_json(config.label_mapper)
    task_c = DataReader.load_json(config.umls_task_c_train)
    task_c_new = []
    for item in task_c:
        text_h_label, text_t_label = "", ""
        label = 'yes' if item['label'] == 'correct' else 'no'
        for key, word_sets in label_mapper.items():
            word_sets_lower = [word for word in word_sets]
            if item['h'] in word_sets_lower:
                text_h_label = key
            elif item['t'] in word_sets_lower:
                text_t_label = key
            if text_h_label != "" and text_t_label != "":
                break
        if text_h_label != "" and text_t_label != "":
            task_c_new.append({"label-triples": [text_h_label, text_t_label, label], "label-names": item, "used": False})
    data_labels = set([data['type-label'] for data in dataset_json])
    task_c_labels = set([label for data in task_c_new for label in data['label-triples']])
    intersect = data_labels.intersection(task_c_labels)
    print("dataset types:", len(data_labels))
    print("Task_c train set types:", len(task_c_labels))
    print("intersection:", len(intersect))

    for data in dataset_json:
        data['task-c'] = False
    for task_c_data in task_c_new:
        search_type_h, search_type_t = task_c_data['label-triples'][0], task_c_data['label-triples'][1]
        for index, data in enumerate(dataset_json):
            if not data['task-c'] and not data['negative']:
                if search_type_h == data['type-label'] or search_type_t == data['type-label']:
                    dataset_json[index]['task-c'] = True
                    dataset_json[index]['task-c-items'] = task_c_data['label-names']
    return dataset_json

if __name__=="__main__":
    config = BaseConfig(neg_per_class=3).get_args("wn18rr")
    custom_train_dataset = build_wn(config)
    DataWriter.write_json(custom_train_dataset, config.fsl_train_data)

    config = BaseConfig(neg_per_class=3).get_args("geonames")
    custom_train_dataset = build_geonames(config)
    custom_train_dataset = add_task_b_info_geonames(config, custom_train_dataset)
    DataWriter.write_json(custom_train_dataset, config.fsl_train_data)

    config = BaseConfig(neg_per_class=3).get_args("umls")
    custom_train_dataset = build_umls(config)
    custom_train_dataset = add_task_b_info_umls(config, custom_train_dataset)
    custom_train_dataset = add_task_c_info_umls(config, custom_train_dataset)
    DataWriter.write_json(custom_train_dataset, config.fsl_train_data)
