from configuration import BaseConfig
from datahandler import DataReader, DataWriter
import pandas as pd
from src import geoname_taxonomy_recursive
import os
from src import make_levels_cleaner_fb


def make_wn18rr(config):
    print(config.relations_to_ignore)

    def make_replacements(df, id2name_, name2defs_):
        df = df.replace(id2name_)
        df["head-def"] = df['head'].map(name2defs_)
        df["tail-def"] = df['tail'].map(name2defs_)
        df['head-entity-type'] = df['head'].apply(lambda X: X.split("_")[-2])
        df['tail-entity-type'] = df['tail'].apply(lambda X: X.split("_")[-2])
        df = df.drop(df[df['relation'].isin(config.relations_to_ignore)].index)
        return df

    def make_entity_detection_dataset(df):
        head_df = df[['head', "head-entity-type"]]
        head_df.rename(columns={"head":"entity", "head-entity-type":"type"}, inplace=True) 
        tail_df = df[['tail', "tail-entity-type"]]
        tail_df.rename(columns={"tail":"entity", "tail-entity-type":"type"}, inplace=True)
        df = pd.concat([head_df, tail_df])
        print(f"ENTITY DETECT: The size of new df is:{df.shape[0]}")
        df = df.drop_duplicates()
        print(f"ENTITY DETECT: The size of new df after duplicate removals is:{df.shape[0]}")
        return df

    train, test, valid, definitions = DataReader.load_csv(config.raw_train, sep='\t', names=["head", "relation", "tail"]), \
                                      DataReader.load_csv(config.raw_test, sep='\t',  names=["head", "relation", "tail"]), \
                                      DataReader.load_csv(config.raw_valid, sep='\t', names=["head", "relation", "tail"]), \
                                      DataReader.load_csv(config.definition, sep='\t',  names=['entity_id', 'entity', 'definitions'])
    id2name = definitions.set_index('entity_id').to_dict()['entity']
    name2defs = definitions.set_index('entity').to_dict()['definitions']
    train, test, valid = make_replacements(train, id2name, name2defs), \
                         make_replacements(test, id2name, name2defs), \
                         make_replacements(valid, id2name, name2defs)
    DataWriter.write_df(train, path=config.processed_train)
    DataWriter.write_df(test, path=config.processed_test)
    DataWriter.write_df(valid, path=config.processed_valid)

    train_e, test_e, valid_e = make_entity_detection_dataset(train), \
                               make_entity_detection_dataset(test), \
                               make_entity_detection_dataset(valid)
    DataWriter.write_df(train_e, path=config.processed_entity_train)
    DataWriter.write_df(test_e, path=config.processed_entity_test)
    DataWriter.write_df(valid_e, path=config.processed_entity_valid)


def make_fb15k_237(config):

    def add_levels(items_lst, mapper):
        mapped_levels_lst = []
        for items in items_lst:
            mapped_level = []
            if str(items) != 'nan':
                for item in eval(str(items)):
                    if mapper.get(item, "NA") != "NA":
                        mapped_level.append(mapper.get(item))
            mapped_levels_lst.append(list(set(mapped_level)))
        return mapped_levels_lst

    def add_levels_to_df(df, level1, level2, level3):
        df['level-1'] = add_levels(df['entclass'].tolist(), level1)
        df['level-2'] = add_levels(df['entclass'].tolist(), level2)
        df['level-3'] = add_levels(df['entclass'].tolist(), level3)
        return df
        
    def convert_mid2names(df, mid2name_mapper, dataset_name):
        print("-"*40)
        print(f"working on dataset in converting MID2Names: {dataset_name}")
        df['head-mid2name'] = df['head-mid'].map(mid2name_mapper)
        df['tail-mid2name'] = df['tail-mid'].map(mid2name_mapper)
        old_size = df.shape[0]
        df = df.dropna()
        print(f"Number of NANS in {dataset_name} set is: {old_size - df.shape[0]}")
        print(f"Current size of {dataset_name} is:{df.shape[0]}")
        return df

    def creat_freebase_fb15kbased_mapper(dir_path):
        mid2names_dict = {}
        for js_file in os.listdir(dir_path):
            js_file_path = os.path.join(dir_path, js_file)
            fold_data = DataReader.load_json(js_file_path)
            for key, folds in fold_data.items():
                mid2names_dict_lst = []
                for fold in folds:
                    try:
                        _, rel, tail = fold[2:-6].split("\\t")
                        if "type.object.name" in rel and "@en" in tail:
                            mid2names_dict_lst.append(tail.split("@")[0][1:-1])
                    except:
                        continue
                if len(mid2names_dict_lst) != 0:
                    mid2names_dict["/"+key.replace(".", "/")] = mid2names_dict_lst
        mid2names_dict = {key: values[0] for key, values in mid2names_dict.items()}
        return mid2names_dict

    def create_mid2entclass_mapper(freebase_types_path, freebase_hierarchy):
        print("-"*40)
        type_df = DataReader.load_csv(freebase_types_path, sep='\t', names=["mid", "wordnet_type"])
        hierarchy = DataReader.load_json(freebase_hierarchy)
        
        wordnet_types_to_consider = []
        for _, level_dict in hierarchy.items():
            for wordnet_type, _ in level_dict.items():
                wordnet_types_to_consider.append(wordnet_type)
        wordnet_types_to_consider = list(set(wordnet_types_to_consider))    

        type_df = type_df[type_df['wordnet_type'].isin(wordnet_types_to_consider)]
        print("Shape of WordNet types dataframe is:", type_df.shape[0])
        print("Number of unique values for WordNet types are:", len(type_df['wordnet_type'].unique()))

        mid2entclass_mapper = {}
        for mid, wordnet_type in zip(type_df['mid'].tolist(), type_df['wordnet_type'].tolist()):
            if mid not in mid2entclass_mapper:
                mid2entclass_mapper[mid] = []
            mid2entclass_mapper[mid].append(wordnet_type)
        print(f"At the end size of MID2EntClass mapper is:{len(mid2entclass_mapper)}")
        return mid2entclass_mapper

    def convert_mid2ent_classes(df, mid2entclass_mapper, dataset_name):
        print("-"*40)
        print(f"working on dataset in converting MID2EntClass: {dataset_name}")
        df['head-mid2entclass'] = df['head-mid'].map(mid2entclass_mapper)
        df['tail-mid2entclass'] = df['tail-mid'].map(mid2entclass_mapper)
        old_size = df.shape[0]
        df = df.dropna()
        print(f"Number of NANS in {dataset_name} set is: {old_size - df.shape[0]}")
        print(f"Current size of {dataset_name} is:{df.shape[0]}")
        return df

    def create_level_mapper(freebase_hierarchy):
        hierarchy = DataReader.load_json(freebase_hierarchy)
        level_mappers = {"level-1":{}, "level-2":{}, "level-3":{}}
        for level, level_dict in hierarchy.items():
            for wordnet_type, level_class in level_dict.items():
                level_mappers[level][wordnet_type] = level_class
        return level_mappers['level-1'], level_mappers['level-2'], level_mappers['level-3']

    def make_entity_df(df, dataset_name):
        df_ent = pd.concat([
                df[['head-mid', 'head-mid2name', 'head-mid2entclass']].rename(columns={'head-mid':"mid", 'head-mid2name':"name", 'head-mid2entclass':"entclass"}), 
                df[['tail-mid', 'tail-mid2name', 'tail-mid2entclass']].rename(columns={'tail-mid':"mid", 'tail-mid2name':"name", 'tail-mid2entclass':"entclass"})
                ]).reset_index(drop=True)
        print("-"*40)
        print(f"{dataset_name} size before removing duplicates based on [mid, name] is:{df_ent.shape[0]}")
        df_ent = df_ent.drop_duplicates(subset=['mid', 'name'], keep='first').reset_index()
        print(f"Current size  after droping duplicates is: {df_ent.shape[0]}")
        return df_ent

    # load datasets
    train, test, valid = DataReader.load_csv(config.raw_train, sep='\t', names=["head-mid", "relation", "tail-mid"]), \
                         DataReader.load_csv(config.raw_test, sep='\t',  names=["head-mid", "relation", "tail-mid"]), \
                         DataReader.load_csv(config.raw_valid, sep='\t', names=["head-mid", "relation", "tail-mid"])
    
    # 1. Make replacement for converting MID2Name      ---> this will be for relationship extraction
    # load and create mid2names
    mid2name = creat_freebase_fb15kbased_mapper(dir_path=config.freebase_dumps_dir)
    train, test, valid = convert_mid2names(train, mid2name, "Train"), \
                         convert_mid2names(test,  mid2name, "Test"), \
                         convert_mid2names(valid, mid2name, "Valid")

    # 2. Creating levels mapper using Names for each  ---> This will be for entity type detection
    # load and create mid2entclass mapper
    mid2entclass = create_mid2entclass_mapper(config.freebase_types, config.freebase_hierarchy)
    train, test, valid = convert_mid2ent_classes(train, mid2entclass, "Train"), \
                         convert_mid2ent_classes(test, mid2entclass, "Test"), \
                         convert_mid2ent_classes(valid, mid2entclass, "Valid")

    # save relationship detection datasets first!
    DataWriter.write_df(train[['head-mid', 'relation', 'tail-mid', 'head-mid2name', 'tail-mid2name']], path=config.processed_train_rel)
    DataWriter.write_df(test[['head-mid', 'relation', 'tail-mid', 'head-mid2name', 'tail-mid2name']],  path=config.processed_test_rel)
    DataWriter.write_df(valid[['head-mid', 'relation', 'tail-mid', 'head-mid2name', 'tail-mid2name']],  path=config.processed_valid_rel)

    train_ent, test_ent, valid_ent = make_entity_df(train, "Train"), make_entity_df(test, "Test"), make_entity_df(valid, "Valid")
    wordnet2level1, wordnet2level2, wordnet2level3 = create_level_mapper(config.freebase_hierarchy)

    train_ent, test_ent, valid_ent = add_levels_to_df(train_ent, wordnet2level1, wordnet2level2, wordnet2level3), \
                                     add_levels_to_df(test_ent, wordnet2level1, wordnet2level2, wordnet2level3), \
                                     add_levels_to_df(valid_ent, wordnet2level1, wordnet2level2, wordnet2level3)

    train_ent, test_ent, valid_ent = make_levels_cleaner_fb(train_ent), \
                                     make_levels_cleaner_fb(test_ent), \
                                     make_levels_cleaner_fb(valid_ent)
    # Savings entities
    DataWriter.write_df(train_ent, path=config.processed_test_ent)
    DataWriter.write_df(test_ent, path=config.processed_valid_ent)
    DataWriter.write_df(valid_ent, path=config.processed_train_ent)


def make_geoname(config):
    feature_codes_df = DataReader.load_csv(config.feature_codes, sep='\t', 
                                           names=["feature-code", "name", "description"])
    feature_codes_df = feature_codes_df.drop(feature_codes_df[feature_codes_df['feature-code'].isnull()].index)
    feature_codes_df['level-1'] = feature_codes_df['feature-code'].apply(lambda X: str(X)[0])
    feature_codes_df['level-3'] = feature_codes_df['feature-code'].apply(lambda X: str(X)[2:])

    level2_mapper = {}
    for group, group_df in feature_codes_df.groupby("level-1"):
        group_df_level2_taxonomy = geoname_taxonomy_recursive(group_df['level-3'].tolist(), depth=config.depth)
        print(f"group {group}: number of depth-2 items:‌ {len(group_df_level2_taxonomy)}")
        for depth2_name, depth2_items in group_df_level2_taxonomy.items():
            for depth3_name, depth3_items in depth2_items.items():
                    for depth3_item in depth3_items:
                        level2_mapper[depth3_item] = depth3_name

    feature_codes_df['level-2'] = feature_codes_df['level-3'].map(level2_mapper)
    level3_columns = feature_codes_df.pop("level-3")
    feature_codes_df.insert(5, "level-3", level3_columns)
    DataWriter.write_df(feature_codes_df, path=config.processed_feature_codes)
    
    all_countries_df = DataReader.load_csv(config.all_countries, sep='\t', low_memory=False, 
                                           names=["geonameid", "name", "asciiname", "alternatenames","latitude",
                                                 "longitude", "feature-class", "feature-code", "country-code", "cc2",
                                                 "admin1-code", "admin2-code", "admin3-code", "admin4-code", "population",
                                                 "elevation", "dem", "timezone", "modification-date"])[["name", "asciiname", "country-code",
                                                                                                        "feature-class", "feature-code"]]
    all_countries_df = all_countries_df.drop(all_countries_df[all_countries_df['feature-class'].isnull()].index)
    all_countries_df.rename(columns={"feature-class":"level-1", "feature-code":"level-3"}, inplace=True)
    all_countries_df['level-2'] = all_countries_df['level-3'].map(level2_mapper)
    level3_columns = all_countries_df.pop("level-3")
    all_countries_df.insert(5, "level-3", level3_columns)
    DataWriter.write_df(all_countries_df, path=config.processed_all_countries)


if __name__ == "__main__":
    # config = BaseConfig().get_args(db_name="wn18rr")
    # make_wn18rr(config=config)

    config = BaseConfig(version=2).get_args(db_name="fb15k-237")
    make_fb15k_237(config=config)

    # config = BaseConfig().get_args(db_name="geonames")
    # make_geoname(config=config)
 
 