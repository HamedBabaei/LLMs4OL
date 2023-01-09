from configuration import BaseConfig
from datahandler import DataReader, DataWriter
import pandas as pd
from src import geoname_taxonomy_recursive
import os


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
                # print(items)
                for item in eval(str(items)):
                    if mapper.get(item, "NA") != "NA":
                        mapped_level.append(mapper.get(item))
            mapped_levels_lst.append(list(set(mapped_level)))
        return mapped_levels_lst

    def make_replacements(df, mid2name_, taxonomy_, dataset_name, level_mapper):

        print(f"working on dataset: {dataset_name}")
        df['head-mid2name'] = df['head-mid'].map(mid2name_)
        df['tail-mid2name'] = df['tail-mid'].map(mid2name_)
        df['head-mid2taxonomy'] = df['head-mid'].map(taxonomy_)
        df['tail-mid2taxonomy'] = df['tail-mid'].map(taxonomy_)
        df['head-levels'] = add_levels(df['head-mid2taxonomy'].tolist(),level_mapper)
        # print(df['head-levels'])
        # exit(0)
        df['tail-levels'] = add_levels(df['tail-mid2taxonomy'].tolist(),level_mapper)
        old_size = df.shape[0]
        df = df.dropna()
        new_size = df.shape[0]
        print("Number of nans:", old_size - new_size)
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

    def create_taxonomy_mapper(freebase_types_path, freebase_hierarchy):
        type_df = DataReader.load_csv(freebase_types_path, sep='\t', names=["mid", "type"])
        hierarchy = DataReader.load_json(freebase_hierarchy)
        
        hierarchies = []
        for _, items in hierarchy.items():
            for item in items:
                hierarchies.append(item)
        hierarchies = list(set(hierarchies))    
        
        type_df = type_df[type_df['type'].isin(hierarchies)]
        print("size of unique values in type_df is:", len(type_df['type'].unique()))
        tax_mid, tax_type = type_df['mid'].tolist(), type_df['type'].tolist()
        taxonomy = {}
        for index, mid in enumerate(tax_mid):
            if mid not in taxonomy:
                taxonomy[mid] = []
            taxonomy[mid].append(tax_type[index])
        return taxonomy

    def create_level_mapper(freebase_hierarchy):
        hierarchy = DataReader.load_json(freebase_hierarchy)
        hierarchy_mapper = {}
        for level, classes in hierarchy.items():
            for class_ in classes:
                hierarchy_mapper[class_] = level
        return hierarchy_mapper

    # load datasets
    train, test, valid = DataReader.load_csv(config.raw_train, sep='\t', names=["head-mid", "relation", "tail-mid"]), \
                         DataReader.load_csv(config.raw_test, sep='\t',  names=["head-mid", "relation", "tail-mid"]), \
                         DataReader.load_csv(config.raw_valid, sep='\t', names=["head-mid", "relation", "tail-mid"]), \
    
    # load and create mid2names
    mid2name = creat_freebase_fb15kbased_mapper(dir_path=config.freebase_dumps_dir)

    # load and create taxonomy
    taxonomy = create_taxonomy_mapper(config.freebase_types, config.freebase_hierarchy)
    
    level_mappers = create_level_mapper(config.freebase_hierarchy)
    
    # make the mapping for taxonomy and‌ MID2Name
    train, test, valid = make_replacements(train, mid2name, taxonomy, "Train", level_mappers), \
                         make_replacements(test,  mid2name, taxonomy, "Test", level_mappers) , \
                         make_replacements(valid, mid2name, taxonomy, "Valid", level_mappers)

    # get all MIDs to create MID2WordNet
    all_mids = train['head-mid'].tolist() + train['tail-mid'].tolist() + \
               test['head-mid'].tolist()  + test['tail-mid'].tolist()  + \
               valid['head-mid'].tolist() + valid['tail-mid'].tolist()

    all_mids = list(set(all_mids))
    print("len all mids:", len(all_mids), "\t", all_mids[:3])   
    mids_to_wordnetids = {mid: taxonomy.get(mid, None) for mid in all_mids}
    names2wordnetid = {"mid":[name for name, _ in mids_to_wordnetids.items()],
                       "wordnetid": [wordnetid for _, wordnetid in mids_to_wordnetids.items()]}
    names2wordnetid_df = pd.DataFrame(data=names2wordnetid)
    print(f"number of nans are: {names2wordnetid_df.shape[0] - names2wordnetid_df.dropna().shape[0]}")


    # Savings
    DataWriter.write_df(test, path=config.processed_test)
    DataWriter.write_df(valid, path=config.processed_valid)
    DataWriter.write_df(train, path=config.processed_train)
    DataWriter.write_df(names2wordnetid_df, config.processed_wordnet_taxonomy)



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

    config = BaseConfig().get_args(db_name="fb15k-237")
    make_fb15k_237(config=config)

    # config = BaseConfig().get_args(db_name="geonames")
    # make_geoname(config=config)
 
 