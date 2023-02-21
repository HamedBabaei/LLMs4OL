from configuration import BaseConfig
from datahandler import DataReader, DataWriter


def build_geonames(config):
    pass


def build_umls(config):
    pass


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
