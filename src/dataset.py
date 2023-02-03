
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
    
    def collate_fn(self, batchs):
        batchs_clear = {"sample":[], "label":[]}
        for batch in batchs:
            batchs_clear['sample'].append(batch['sample'])
            batchs_clear['label'].append(batch['label'])
        return batchs_clear
