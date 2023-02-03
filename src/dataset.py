
from torch.utils.data import Dataset

class WNDataset(Dataset):
    def __init__(self, data, template, dataset_type, is_train, label_in_list=True):
        self.data = data
        self.template = self.data['templates'][template]
        self.is_train = is_train
        self.dataset_type = dataset_type
        self.use_sentence =  True if "[SENTENCE]" in self.template else False
        self.label_in_list = label_in_list

        print(f"WNDataset:{'Train-SET' if self.is_train else 'Test-SET'} --- {template}: {self.template}")
    
    def __len__(self):
        return len(self.data[self.dataset_type])
    
    def __repr__(self) -> str:
         return f"WNDataset:{'Train-SET' if self.is_train else 'Test-SET'} --- Template-in-use: {self.template}"
    
    def __getitem__(self, index):
        item = self.data[self.dataset_type][index]
        sample, label = self.template.replace("[A]", item['entity']), item['label']
        if self.label_in_list:
            label = [label]
        if self.use_sentence:
            sample = sample.replace("[SENTENCE]", item['sentence'])
        if self.is_train:
            sample = sample.replace("[MASK]", item['label'])
        return {"sample":sample, "label":label}

    def get_stats(self):
        return self.data['stats']

    def collate_fn(self, batchs):
        batchs_clear = {"sample":[], "label":[]}
        for batch in batchs:
            batchs_clear['sample'].append(batch['sample'])
            batchs_clear['label'].append(batch['label'])
        return batchs_clear

class GeonameDataset(Dataset):
    def __init__(self, data, template, dataset_type, is_train, label_in_list=True):
        self.template = data['templates'][template]
        self.is_train = is_train
        self.level_key = dataset_type
        self.stats = data['stats']
        self.use_country =  True if "[COUNTRY]" in self.template else False
        self.label_in_list = label_in_list
        self.data = []
        level_search_key = "status-in-"+self.level_key
        for sample in data['geonames']:
            if level_search_key in list(sample.keys()):
                if self.is_train and sample[level_search_key] == "train":
                    self.data.append(sample)
                if not self.is_train and sample[level_search_key] == "test":
                    self.data.append(sample)
        print(f"GeonamesDataset:{'Train-SET' if self.is_train else 'Test-SET'}-{self.level_key} --- {template}: {self.template}")
    
    def __len__(self):
        return len(self.data)
    
    def __repr__(self) -> str:
         return f"GeonamesDataset:{'Train-SET' if self.is_train else 'Test-SET'}-{self.level_key} --- Template-in-use: {self.template}"
    
    def __getitem__(self, index):
        item = self.data[index]
        sample, label = self.template.replace("[A]", item['asciname']), item['label-strings-in-'+self.level_key]
        if self.label_in_list:
            label = label
        if self.use_country:
            sample = sample.replace("[COUNTRY]", item['country_name'])
        if self.is_train:
            sample = sample.replace("[MASK]", 'or '.join(item['label-strings-in-'+self.level_key]))
        return {"sample":sample, "label":label}
    
    def get_stats(self):
        return self.stats[self.level_key]

    def collate_fn(self, batchs):
        batchs_clear = {"sample":[], "label":[]}
        for batch in batchs:
            batchs_clear['sample'].append(batch['sample'])
            batchs_clear['label'].append(batch['label'])
        return batchs_clear

class BaselineInferenceDatasetFactory:
    def __new__(CLS, kb_name, data, template) -> Dataset:
        if kb_name == "geonames":
            return GeonameDataset(data=data, template=template, 
                                  dataset_type="level-1", is_train=False, 
                                  label_in_list=True)
        if kb_name == "wn18rr":
            return WNDataset(data=data, template=template, 
                             dataset_type="test", is_train=False, 
                             label_in_list=True)