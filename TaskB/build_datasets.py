from configuration import BaseConfig
from datahandler import DataReader, DataWriter
import re

def build_geonames(config):
    df = DataReader.load_df(config.feature_codes)
    name_mappers = {
        "A": "country, state, or region",
        "H": "stream or lake",
        "L": "parks or areas",
        "P": "city or village",
        "R": "road or railroad",
        "S": "spot, building, or farm",
        "T": "mountain, hill, or rock",
        "U": "undersea",
        "V": "forest or heath"
    }
    text_a_list = df['L1'].tolist()
    text_b_list = df['L2Name'].tolist()
    data_dict = []
    for text_a, text_b in zip(text_a_list, text_b_list):
        data_dict.append({
            "text_a": name_mappers[text_a],
            "text_b": text_b.lower(),
            "label": "correct"
        })
        data_dict.append({
            "text_a": text_b.lower(),
            "text_b": name_mappers[text_a],
            "label": "incorrect"
        })
    DataWriter.write_json(data=data_dict, path=config.processed_hier)
    print("size of processed hierarchy in GeoNames is :", len(data_dict))

def build_umls(config):
    df = DataReader.load_df(config.processed_sn)

    data_tuple = []

    # a=root, b=level-1
    text_a_list = df['Root'].tolist()
    text_b_list = df['Level1Name'].tolist()
    for text_a, text_b in zip(text_a_list, text_b_list):
        if text_b != " " and text_a != " ":
            data_tuple.append((text_a.lower(), text_b.lower()))

    # a=level-1, b=level-2
    text_a_list = df['Level1Name'].tolist()
    text_b_list = df['Level2Name'].tolist()
    for text_a, text_b in zip(text_a_list, text_b_list):
        if text_b != " " and text_a != " ":
            data_tuple.append((text_a.lower(), text_b.lower()))

    # a=level-2  b=level-3
    text_a_list = df['Level2Name'].tolist()
    text_b_list = df['Level3Name'].tolist()
    for text_a, text_b in zip(text_a_list, text_b_list):
        if text_b != " " and text_a != " ":
            data_tuple.append((text_a.lower(), text_b.lower()))

    # a=root  b=level-2
    text_a_list = df['Root'].tolist()
    text_b_list = df['Level2Name'].tolist()
    for text_a, text_b in zip(text_a_list, text_b_list):
        if text_b != " " and text_a != " ":
            data_tuple.append((text_a.lower(), text_b.lower()))

    # a=level-1  b=level-3
    text_a_list = df['Level1Name'].tolist()
    text_b_list = df['Level3Name'].tolist()
    for text_a, text_b in zip(text_a_list, text_b_list):
        if text_b != " " and text_a != " ":
            data_tuple.append((text_a.lower(), text_b.lower()))

    data_tuple = list(set(data_tuple))
    data_dict = []
    for item in data_tuple:
        data_dict.append({
            "text_a": item[0],
            "text_b": item[1],
            "label": "correct"
        })
        data_dict.append({
            "text_a": item[1],
            "text_b": item[0],
            "label": "incorrect"
        })

    DataWriter.write_json(data=data_dict, path=config.processed_hier)
    print("size of processed hierarchy in UMLS is :", len(data_dict))

def build_schema(config):
    def make_words(label):
        words = re.findall(r'[A-Z]?[0-9a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)', label)
        return ' '.join(words)
    def make_subtype(sub_type_url):
        words = sub_type_url.split("/")[-1]
        return make_words(words)

    df = DataReader.load_df(config.raw_types)[["id", "label", "comment", "subTypeOf"]]
    df = df.dropna()
    df['text-b'] = df['label'].apply(make_words)
    df['text-a'] = df['subTypeOf'].apply(make_subtype)

    # if (A, B) and (B, C) then (A, C)
    lsts = [(A,B) for A, B in zip(df['text-a'].tolist(), df['text-b'].tolist())]
    rules = []
    for index, (A, B) in enumerate(lsts):
        rules.append((A, B))
        for b, C in lsts:
            if B == b:
                rules.append((A, C))
    rules = list(set(rules))
    print("size of pairs after adding 'if (A, B) and (B, C) then (A, C)' and duplicatee removals is:", len(rules))
    data_dict = []
    for item in rules:
        data_dict.append({
            "text_a": item[0],
            "text_b": item[1],
            "label": "correct"
        })
        data_dict.append({
            "text_a": item[1],
            "text_b": item[0],
            "label": "incorrect"
        })

    DataWriter.write_json(data=data_dict, path=config.processed_hier)
    print("size of processed hierarchy in SchemaOrg is :", len(data_dict))

if __name__ == "__main__":
    KB_NAMES = {
        'geonames': build_geonames,
        "umls": build_umls,
        "schema": build_schema
    }
    for kb_name, function in KB_NAMES.items():
        CONFIG = BaseConfig().get_args(kb_name=kb_name)
        function(config=CONFIG)
