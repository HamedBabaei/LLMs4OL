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
    config = BaseConfig().get_args(db_name="wn18rr")
    make_wn18rr(config=config)

    # config = BaseConfig().get_args(db_name="geonames")
    # make_geoname(config=config)
 
 