from configuration import BaseConfig
from datahandler import DataReader, DataWriter
from sklearn.model_selection import train_test_split

def train_test_split_hier(config):
    dataset = DataReader.load_json(config.processed_hier)
    datas, labels = dataset, [data['label'] for data in dataset]
    train, test, _, _ = train_test_split(datas, labels , test_size=config.test_size, random_state=config.seed)
    DataWriter.write_json(train, config.processed_train)
    DataWriter.write_json(test, config.processed_test)
    print(f"Train size:{len(train)},  Test size:{len(test)}")

if __name__=="__main__":
    print("Geonames:")
    train_test_split_hier(config=BaseConfig().get_args(kb_name='geonames'))
    print("Schema:")
    train_test_split_hier(config=BaseConfig().get_args(kb_name='schema'))
    print("UMLS:")
    train_test_split_hier(config=BaseConfig().get_args(kb_name='umls'))