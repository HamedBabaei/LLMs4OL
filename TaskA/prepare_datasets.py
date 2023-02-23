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
        # df = df.drop(df[df['relation'].isin(config.relations_to_ignore)].index)
        # df = df.drop(df[df['head-entity-type'].isin(config.entity_class_to_ignore)].index)
        # df = df.drop(df[df['tail-entity-type'].isin(config.entity_class_to_ignore)].index)
        return df

    def make_entity_detection_dataset(df, count=-1, use_sampling=False):
        df = pd.concat([
                    df[['head', "head-entity-type", "head-def"]].rename(columns={"head":"entity", 
                                                                                 "head-entity-type":"type", 
                                                                                 "head-def":"definition"}), 
                    df[['tail', "tail-entity-type", "tail-def"]].rename(columns={"tail":"entity", 
                                                                                 "tail-entity-type":"type", 
                                                                                 "tail-def":"definition"})
                ]).reset_index(drop=True)
        
        df = df.drop_duplicates(subset=['entity', 'type'], keep='first')
        if use_sampling:
            dfs = []
            for type_name, type_df in df.groupby("type"):
                if type_df.shape[0] <= count:
                    dfs.append(type_df)
                else:
                    dfs.append(type_df.sample(count, random_state=222, replace=False))
            df = pd.concat(dfs)
            df = df.drop_duplicates(subset=['entity', 'type'], keep='first')
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
    train_e, test_e, valid_e = make_entity_detection_dataset(train, count=-1, use_sampling=False), \
                               make_entity_detection_dataset(test, count=-1, use_sampling=False), \
                               make_entity_detection_dataset(valid, count=-1, use_sampling=False)

    new_train = train[train['head'].isin(train_e['entity'].tolist()) & train['tail'].isin(train_e['entity'].tolist())] 
    new_test = test[test['head'].isin(test_e['entity'].tolist()) & test['tail'].isin(test_e['entity'].tolist())] 
    new_valid = valid[valid['head'].isin(valid_e['entity'].tolist()) & valid['tail'].isin(valid_e['entity'].tolist())] 
    
    print(f"The size of relation detection train set is:{new_train.shape[0]}")
    print(f"The size of relation detection test set is:{new_test.shape[0]}")
    print(f"The size of relation detection valid set is:{new_valid.shape[0]}")

    print(f"The size of entity type detection train set is:{train_e.shape[0]}")
    print(f"The size of entity type detection test set is:{test_e.shape[0]}")
    print(f"The size of entity type detection valid set is:{valid_e.shape[0]}")

    DataWriter.write_df(new_train, path=config.processed_train)
    DataWriter.write_df(new_test, path=config.processed_test)
    DataWriter.write_df(new_valid, path=config.processed_valid)

    DataWriter.write_df(train_e, path=config.processed_entity_train)
    DataWriter.write_df(test_e, path=config.processed_entity_test)
    DataWriter.write_df(valid_e, path=config.processed_entity_valid)


def make_geoname(config):

    def make_level2_reduction(df, max_class_no):
        dfs = []
        for group_name, df in df.groupby("level-1"):
            if len(df['level-2'].unique()) > max_class_no:
                df = df[df['level-2'].isin(list(df['level-2'].value_counts()[:max_class_no].index))]
            dfs.append(df)            
        df = pd.concat(dfs)
        return df

    def make_level3_reduction(df, count_no):
        dfs = []
        for group_name, df in df.groupby("level-1"):
            if df.shape[0] > count_no:
                df = df.sample(count_no, random_state=222, replace=False)
            dfs.append(df)            
        df = pd.concat(dfs)
        return df

    feature_codes_df = DataReader.load_csv(config.feature_codes, sep='\t', 
                                           names=["feature-code", "name", "description"])
    feature_codes_df = feature_codes_df.drop(feature_codes_df[feature_codes_df['feature-code'].isnull()].index)
    # feature_codes_df['level-1'] = feature_codes_df['feature-code'].apply(lambda X: str(X)[0])
    # feature_codes_df['level-3'] = feature_codes_df['feature-code'].apply(lambda X: str(X)[2:])
    #
    # level2_mapper = {}
    # for group, group_df in feature_codes_df.groupby("level-1"):
    #     group_df_level2_taxonomy = geoname_taxonomy_recursive(group_df['level-3'].tolist(), depth=config.depth)
    #     print(f"group {group}: number of depth-2 items: {len(group_df_level2_taxonomy)}")
    #     for depth2_name, depth2_items in group_df_level2_taxonomy.items():
    #         for depth3_name, depth3_items in depth2_items.items():
    #                 for depth3_item in depth3_items:
    #                     level2_mapper[depth3_item] = depth3_name
    #
    # feature_codes_df['level-2'] = feature_codes_df['level-3'].map(level2_mapper)
    # level3_columns = feature_codes_df.pop("level-3")
    # feature_codes_df.insert(5, "level-3", level3_columns)
    
    
    all_countries_df = DataReader.load_csv(config.all_countries, sep='\t', low_memory=False, 
                                           names=["geonameid", "name", "asciiname", "alternatenames","latitude",
                                                 "longitude", "feature-class", "feature-code", "country-code", "cc2",
                                                 "admin1-code", "admin2-code", "admin3-code", "admin4-code", "population",
                                                 "elevation", "dem", "timezone", "modification-date"])[["name", "asciiname", "country-code",
                                                                                                        "feature-class", "feature-code"]]
    all_countries_df = all_countries_df.drop(all_countries_df[all_countries_df['feature-class'].isnull()].index)
    all_countries_df = all_countries_df.drop(all_countries_df[all_countries_df['feature-code'].isnull()].index)
    all_countries_df = all_countries_df.drop_duplicates()
    all_countries_df.rename(columns={"feature-class":"level-1", "feature-code":"level-2"}, inplace=True)
    # all_countries_df['level-2'] = all_countries_df['level-3'].map(level2_mapper)
    # level3_columns = all_countries_df.pop("level-3")
    # all_countries_df.insert(5, "level-3", level3_columns)

    # all_countries_df = make_level2_reduction(all_countries_df, max_class_no=10)
    # all_countries_df = make_level3_reduction(all_countries_df, count_no=1_000_000)

    print(f"Szie of dataset is:{all_countries_df.shape[0]:_}")
    print("Level 1 class FQs:\n", all_countries_df['level-1'].value_counts())

    DataWriter.write_df(feature_codes_df, path=config.processed_feature_codes)
    DataWriter.write_df(all_countries_df, path=config.processed_all_countries)


def make_umls(config):
    def mkdir(path):
        if not os.path.exists(path):
            os.mkdir(path)

    def cleaner(string):
        rserved_words = ["inverse", "of", "has", "as", "from", "to", "by", "is"]
        words = string.split("_")
        if len(words) == 1:
            return string
        
        new_words = []
        for word in words:
            if word not in rserved_words:
                new_words.append(word)
        return "_".join(new_words)

    def filter_based_on_sab(umls_rel, umls_entity, sab, rel_threshold=1000):
        sab_rel_df = umls_rel[umls_rel['SAB-CUI1'].isin([sab]) & umls_rel['SAB-CUI2'].isin([sab])].reset_index()
        # sab_rel_df['RELA'] = sab_rel_df['RELA'].apply(cleaner)
        # sab_rel_df = sab_rel_df[sab_rel_df['RELA'].isin(list(sab_rel_df['RELA'].value_counts().loc[lambda X: X >= rel_threshold].keys()))].reset_index()
        # print(f"# of samples in {sab} relation dataset is : {sab_rel_df.shape[0]:_}")
        sab_ents_list = sab_rel_df['CUI1'].tolist() + sab_rel_df['CUI2'].tolist()
        sab_ents_list = list(set(sab_ents_list))
        sab_ent_df = umls_entity[umls_entity['CUI'].isin(sab_ents_list)].reset_index()
        print(f"# of samples in {sab} entity detection dataset is: {sab_ent_df.shape[0]:_}")
        return sab_rel_df, sab_ent_df
    
    umls_rel_df, umls_entity_df = DataReader.load_df(config.raw_umls_rel), DataReader.load_df(config.raw_umls_entity)
    
    for sab in config.sources_to_consider:
        print(f"{sab} sub dataset stats:")
        sab_path = os.path.join(config.umls_processed_dir, sab)
        mkdir(sab_path)
        umls_rel_sab_df, umls_ent_sab_df = filter_based_on_sab(umls_rel_df, umls_entity_df, sab)
        # print("# of unique relations:", len(umls_rel_sab_df['RELA'].value_counts()))
        # DataWriter.write_df(umls_rel_sab_df, os.path.join(sab_path, "UMLS_" + sab + "_REL.csv"))
        DataWriter.write_df(umls_ent_sab_df, os.path.join(sab_path, "UMLS_" + sab + "_ENT.csv"))
        print("-"*40)

if __name__ == "__main__":
    config = BaseConfig(version=3).get_args(kb_name="wn18rr")
    make_wn18rr(config=config)

    config = BaseConfig(version=3).get_args(kb_name="geonames")
    make_geoname(config=config)

    config = BaseConfig(version=3).get_args(kb_name="umls")
    make_umls(config=config)

