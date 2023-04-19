
class BaseDataset:
    pass

class WN(BaseDataset):
    pass

class GeoNames(BaseDataset):
    pass

class UMLS(BaseDataset):
    pass

class DatasetFactory:

    def __new__(self, dataset):
        datasets = {
            "wn": WN,
            "GeoNames": GeoNames,
            "UMLS": UMLS
        }
        return datasets[dataset]


