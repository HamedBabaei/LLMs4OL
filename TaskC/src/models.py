import openprompt
from openprompt.plms import ModelClass
from openprompt.plms.lm import LMTokenizerWrapper
from transformers import BartTokenizer, BartConfig, BartForConditionalGeneration
from openprompt.data_utils import InputExample
from openprompt.plms import load_plm
from openprompt.prompts import ManualTemplate, ManualVerbalizer
from openprompt import PromptForClassification, PromptDataLoader
import torch
from tqdm import tqdm

openprompt.plms._MODEL_CLASSES['bart']= ModelClass(**{"config":BartConfig,
                                                      "tokenizer": BartTokenizer,
                                                      "model": BartForConditionalGeneration,
                                                      "wrapper": LMTokenizerWrapper})
class ZeroShotPromptClassifier:

    def __init__(self, model_name, model_path, dataset, template, label_mapper, device):
        plm, tokenizer, model_config, wrapper_class = load_plm(model_name=model_name, model_path=model_path)
        self.dataset = self.build_dataset(dataset)
        self.device = device
        prompt_template = ManualTemplate(
            text=template,
            tokenizer=tokenizer,
        )
        self.classes = list(label_mapper.keys())
        prompt_verbalizer = ManualVerbalizer(
            classes=self.classes,
            label_words=label_mapper,
            tokenizer=tokenizer,
        )

        self.prompt_model = PromptForClassification(
            template=prompt_template,
            plm=plm,
            verbalizer=prompt_verbalizer,
            freeze_plm=True,
            plm_eval_mode=True
        )
        if self.device != "cpu":
            self.prompt_model = self.prompt_model.to(self.device)
        if model_name == "t5":
            self.data_loader = PromptDataLoader(dataset=self.dataset['X'], template=prompt_template, tokenizer= tokenizer,
                               tokenizer_wrapper_class= wrapper_class, max_seq_length=256, decoder_max_length=3,
                               batch_size=1, shuffle=False, teacher_forcing=False, predict_eos_token=False,
                               truncate_method="head")
        elif model_name == "bert":
            self.data_loader = PromptDataLoader(dataset=self.dataset['X'], template=prompt_template, tokenizer=tokenizer,
                                                tokenizer_wrapper_class=wrapper_class, shuffle=False)
        elif model_name == "bart":
            self.data_loader = PromptDataLoader(dataset=self.dataset['X'], template=prompt_template, tokenizer=tokenizer,
                                                tokenizer_wrapper_class=wrapper_class,  max_seq_length=256, decoder_max_length=3,
                                                batch_size=1, shuffle=False, teacher_forcing=False, predict_eos_token=False,
                                                truncate_method="head")
        elif model_name == "gpt2":
            self.data_loader = PromptDataLoader(dataset=self.dataset['X'], template=prompt_template, tokenizer=tokenizer,
                                                tokenizer_wrapper_class=wrapper_class, max_seq_length=256, batch_size=1, shuffle=False)

    def test(self):
        y_preds, logits = [], []
        self.prompt_model.eval()
        with torch.no_grad():
            for inputs in tqdm(self.data_loader):
                if self.device != "cpu":
                    inputs = inputs.to(self.device)
                logit = self.prompt_model(inputs)
                preds = torch.argmax(logit, dim=-1)
                if self.device != "cpu":
                    preds = preds.cpu().tolist()[0]
                y_preds.append(self.classes[preds])
        return self.dataset['Y'], y_preds

    def build_dataset(self, dataset):
        # "h": "Amino Acid Sequence",
        # "r": "result_of",
        # "t": "Cell or Molecular Dysfunction",
        # "label": "incorrect",
        dataset_dict = {"X":[], "Y":[]}
        for data in dataset:
            text_a = f"{data['h'].lower()} is {data['r'].replace('_', ' ')} {data['t'].lower()}"
            dataset_dict['X'].append(InputExample(text_a=text_a))
            dataset_dict['Y'].append(data['label'])
        return dataset_dict

    def get_data_loader(self):
        pass
