from configuration import BaseConfig
from datahandler import DataReader, DataWriter
from itertools import groupby
import pandas as pd


def build_geonames(config):
    geo_df = DataReader.load_csv(config.raw_feature_codes,
                                 sep='\t', names=["Code", "Name", "Definition"])
    l1_mapper = {
        "A": ["country", "state", "region"], "H": ["stream", "lake"], "L": ["parks", "area"],
        "P": ["city", "village"], "R": ["road", "railroad"], "S": ["spot", "building", "farm"],
        "T": ["mountain", "hill", "rock"], "U": ["undersea"], "V": ["forest", "heath"]
    }
    geo_df['L1'] = geo_df['Code'].apply(lambda X: X[0])
    geo_df['L1Name'] = geo_df['L1'].apply(lambda X: l1_mapper[X])
    geo_df['L2'] = geo_df['Code'].apply(lambda X: X[2:])
    geo_df['L2Name'] = geo_df['Name']
    geo_df = geo_df.drop(['Name'], axis=1)
    DataWriter.write_df(geo_df, path=config.feature_codes)


def build_umls(config, return_df=False):
    def grouping(original_items: list, end: int):
        def util_func(x): return x[:end]
        temp = sorted(original_items, key=util_func)
        res = [list(ele) for i, ele in groupby(temp, util_func)]
        return res

    umls_js = DataReader.load_json(config.raw_sn)
    # Create A, B
    end = 1
    groups1 = grouping(original_items=list(umls_js['STN2STR'].keys()), end=end)
    group_dict = {}
    for group in groups1:
        head = min(group)
        group.remove(head)
        group_dict[head] = group

    # Create A1, A2, B1, B2
    end = 2
    group_dict_root = {}
    for group_head, group_items in group_dict.items():
        groups = grouping(original_items=group_items, end=end)
        group_dict_temp = {}
        for group in groups:
            head = min(group)
            group.remove(head)
            group_dict_temp[head] = group
        group_dict_root[group_head] = group_dict_temp
    group_dict = group_dict_root.copy()

    # Create A1.1, A2.1, B1.1, B2.1..
    end = 4
    group_dict_root = {}
    for group_head1, group_items1 in group_dict.items():  # A [A1, A2]          B [B1, B2]
        group_dict_root[group_head1] = {}
        for group_head, group_items in group_items1.items():  # A1: [List]   A2: [List]
            group_dict_root[group_head1][group_head] = {}
            groups = grouping(original_items=group_items, end=end)
            for group in groups:
                head = min(group)
                group.remove(head)
                group_dict_root[group_head1][group_head][head] = group
    group_dict = group_dict_root.copy()
    new_group_dict = {"Root": [], "RootName": [], "Level1": [], "Level1Name": [],
                      "Level2": [], "Level2Name": [], "Level3": [], "Level3Name": []}

    for group_head1, group_items1 in group_dict.items():  # A [A1, A2]                    ROOT
        for group_head2, group_items2 in group_items1.items():  #  A1: [A1.1 A1.2 ...]     LEVEL 1
            for group_head3, group_item3 in group_items2.items():  # A1.1 [LIST]  A1.2 []   LEVEL 2
                if len(group_item3) != 0:  # Items are LEVEL-3
                    for item in group_item3:
                        new_group_dict['Root'].append(group_head1)
                        new_group_dict['RootName'].append(umls_js['STN2STR'][group_head1])
                        new_group_dict['Level1'].append(group_head2)
                        new_group_dict['Level1Name'].append(umls_js['STN2STR'][group_head2])
                        new_group_dict['Level2'].append(group_head3)
                        new_group_dict['Level2Name'].append(umls_js['STN2STR'][group_head3])
                        new_group_dict['Level3'].append(item)
                        new_group_dict['Level3Name'].append(umls_js['STN2STR'][item])
                else:
                    new_group_dict['Root'].append(group_head1)
                    new_group_dict['RootName'].append(umls_js['STN2STR'][group_head1])
                    new_group_dict['Level1'].append(group_head2)
                    new_group_dict['Level1Name'].append(umls_js['STN2STR'][group_head2])
                    new_group_dict['Level2'].append(group_head3)
                    new_group_dict['Level2Name'].append(umls_js['STN2STR'][group_head3])
                    new_group_dict['Level3'].append("  ")
                    new_group_dict['Level3Name'].append("  ")

    if return_df:
        return pd.DataFrame(new_group_dict)
    else:
        DataWriter.write_csv(new_group_dict, path=config.processed_sn)

def build_umls_for_medcin(config):
    umls = build_umls(config, return_df=True)
    unvalids = {
        "A": "Entity",
        "A1.2": "Anatomical Structure",
        "A1.1": "Organism",
        "A1": "Physical Object",
        "A2": "Conceptual Entity",
        "B": "Event",
        "B2.2": "Natural Phenomenon or Process",
        "A2.9": "Group"
    }

    name_mappers = {name: "  " for name in unvalids.values()}
    label_mappers = {key: "  " for key in unvalids.keys()}
    def name_mapper(name):
        if name_mappers.get(name, "NA") != "NA":
            return name_mappers[name]
        else:
            return name
    def label_mapper(label):
        if label_mappers.get(label, "NA") != "NA":
            return label_mappers[label]
        else:
            return label

    for column in list(umls.columns):
        if "Name" in column:
            umls[column] = umls[column].apply(name_mapper)
        else:
            umls[column] = umls[column].apply(label_mapper)
    DataWriter.write_csv(umls, path=config.processed_sn)


if __name__ == "__main__":
    KB_NAMES = {
        'geonames': build_geonames,
        "nci": build_umls,
        "medcin": build_umls,
        "snomedct_us": build_umls
    }
    for kb_name, function in KB_NAMES.items():
        CONFIG = BaseConfig().get_args(kb_name=kb_name)
        function(config=CONFIG)