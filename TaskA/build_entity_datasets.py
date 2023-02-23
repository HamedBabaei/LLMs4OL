from configuration import BaseConfig
from src import EntityDatasetBuilderFactory
from datahandler import DataReader, DataWriter


if __name__=="__main__":
    dataset_builder = EntityDatasetBuilderFactory(loader=DataReader)

    # config = BaseConfig(version=3).get_args(kb_name="wn18rr")
    # wn_builder = dataset_builder(config=config)
    # dataset_json, dataset_stats = wn_builder.build()
    # DataWriter.write_json(data=dataset_json,
    #                       path=config.entity_path)
    # DataWriter.write_json(data=dataset_stats,
    #                       path=config.dataset_stats)

    config = BaseConfig(version=3).get_args(kb_name="geonames")
    geo_builder = dataset_builder(config=config)
    dataset_json, dataset_stats = geo_builder.build()
    DataWriter.write_json(data=dataset_json,
                          path=config.entity_path)
    DataWriter.write_json(data=dataset_stats,
                          path=config.dataset_stats)

    # config = BaseConfig(version=3).get_args(kb_name="umls")
    # umls_builder = dataset_builder(config=config)
    # dataset_json = umls_builder.build()
    # for kb in list(dataset_json.keys()):
    #     DataWriter.write_json(data=dataset_json[kb],
    #                         path=BaseConfig(version=2).get_args(kb_name=kb.lower()).entity_path)
