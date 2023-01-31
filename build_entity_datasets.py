from configuration import BaseConfig
from src import EntityDatasetBuilderFactory
from datahandler import DataReader, DataWriter


if __name__=="__main__":
    dataset_builder = EntityDatasetBuilderFactory(loader=DataReader)

    config = BaseConfig(version=2).get_args(db_name="wn18rr")
    wn_builder = dataset_builder(config=config)
    dataset_json = wn_builder.build()
    DataWriter.write_json(data=dataset_json, 
                          path=config.entity_path_template.replace("[DATASET]", config.dataset))
    