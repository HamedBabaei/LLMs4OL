
from openprompt.plms import load_plm, ModelClass
from openprompt.plms.lm import LMTokenizerWrapper
from transformers import BartTokenizer, BartConfig, BartForConditionalGeneration, \
                         BloomForCausalLM, BloomConfig, BloomTokenizerFast, \
                         LlamaForCausalLM, LlamaConfig, LlamaTokenizer

from openprompt.data_utils import InputExample
from openprompt.prompts import ManualTemplate, ManualVerbalizer
from openprompt import PromptForClassification, PromptDataLoader
from openai.embeddings_utils import cosine_similarity, get_embedding
from typing import List, Optional
from tqdm import tqdm
import openprompt
import torch
import openai
import time


class BloomTokenizer(BloomTokenizerFast):
    def get_special_tokens_mask(
            self, token_ids_0: List, token_ids_1: Optional[List] = None, already_has_special_tokens: bool = False
    ) -> List[int]:
        """
        Retrieves sequence ids from a token list that has no special tokens added. This method is called when adding
        special tokens using the tokenizer `prepare_for_model` or `encode_plus` methods.

        Args:
            token_ids_0 (`List[int]`):
                List of ids of the first sequence.
            token_ids_1 (`List[int]`, *optional*):
                List of ids of the second sequence.
            already_has_special_tokens (`bool`, *optional*, defaults to `False`):
                Whether or not the token list is already formatted with special tokens for the model.

        Returns:
            A list of integers in the range [0, 1]: 1 for a special token, 0 for a sequence token.
        """
        if already_has_special_tokens:
            if token_ids_1 is not None:
                raise ValueError(
                    "You should not supply a second sequence if the provided sequence of "
                    "ids is already formatted with special tokens for the model."
                )
            return super().get_special_tokens_mask(
                token_ids_0=token_ids_0, token_ids_1=token_ids_1, already_has_special_tokens=True
            )
        return [0] * ((len(token_ids_1) if token_ids_1 else 0) + len(token_ids_0))

openprompt.plms._MODEL_CLASSES['bloom']= ModelClass(**{"config": BloomConfig,
                                                       "tokenizer": BloomTokenizer,
                                                       "model": BloomForCausalLM,
                                                       "wrapper": LMTokenizerWrapper})

openprompt.plms._MODEL_CLASSES['bart']= ModelClass(**{"config":BartConfig,
                                                      "tokenizer": BartTokenizer,
                                                      "model": BartForConditionalGeneration,
                                                      "wrapper": LMTokenizerWrapper})


openprompt.plms._MODEL_CLASSES['llama']= ModelClass(**{"config": LlamaConfig,
                                                       "tokenizer": LlamaTokenizer,
                                                       "model": LlamaForCausalLM,
                                                       "wrapper": LMTokenizerWrapper})

def load_llama(model_name, model_path, specials_to_add = None):
    model_config = LlamaConfig.from_pretrained(model_path)
    model = LlamaForCausalLM.from_pretrained(model_path,
                                             config=model_config,
                                             load_in_8bit=False,
                                             torch_dtype=torch.float16,
                                             device_map="balanced")
    tokenizer = LlamaTokenizer.from_pretrained(model_path,  padding_side='left')
    tokenizer.pad_token = tokenizer.eos_token
    wrapper = LMTokenizerWrapper
    return model, tokenizer, model_config, wrapper


class ZeroShotPromptClassifier:

    def __init__(self, model_name, model_path, dataset, template, label_mapper, device):
        if model_name == 'llama':
            plm, tokenizer, model_config, wrapper_class = load_llama(model_name=model_name, model_path=model_path)
        else:
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
        elif model_name == "bloom" or model_name=='llama':
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
        dataset_dict = {"X":[], "Y":[]}
        for data in dataset:
            dataset_dict['X'].append(InputExample(text_a=data['text_a'], text_b=data['text_b']))
            dataset_dict['Y'].append(data['label'])
        return dataset_dict

class GPT3Inferencer:
    def __init__(self, model_name, model_path, dataset, template, label_mapper, device):
        self.model_path = model_path
        self.dataset = dataset
        self.template = template
        self.gpt3_template = "Identify whether the following statement is true or false:\n\nStatement: [TEMPLATE]"
        self.gpt_max_tokens = 10

    def check_all_is_done(self, results):
        for result in results:
            if result['check'] == False:
                return False
        return True

    def test(self):
        results = []
        for index, data in enumerate(self.dataset):
            results.append({"check": False})

        assert self.check_all_is_done(results) == False

        while not self.check_all_is_done(results):
            for index, data in tqdm(enumerate(self.dataset)):
                if results[index]['check'] != True:
                    try:
                        results[index]['result'] = self.make_prediction(template=self.template,
                                                                        gpt3_template=self.gpt3_template,
                                                                        data=data)
                        results[index]['check'] = True
                    except Exception as err:
                        print(f"UNexpected {err}, {type(err)}")
                        print("Going to sleep for 5 second!")
                        time.sleep(5)
        return results

    def make_prediction(self, template, gpt3_template, data):
        # {'h': 'Organism',
        #  'r': 'interacts_with',
        #  't': 'Organism',
        #  'label': 'correct',
        #  'triples': ['T001', 'T142', 'T001']}
        prompt = template.replace("{\"placeholder\": \"text_a\"}", data['text_a'])\
                         .replace("{\"placeholder\": \"text_b\"}", data['text_b'])\
                         .replace(" {\"mask\"} .", ": ")\
                         .replace(". This statement is", ".\nThis statement is")
        prompt = gpt3_template.replace("[TEMPLATE]", prompt)

        response = openai.Completion.create(
            model=self.model_path,
            prompt=prompt,
            temperature=0.7,
            max_tokens=self.gpt_max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        result = {"data": data, "prompt": prompt, "response": response}
        return result

    def get_data_loader(self):
        pass

class GPT4Inferencer(GPT3Inferencer):
    def make_prediction(self, template, gpt3_template, data):
        # {'h': 'Organism',
        #  'r': 'interacts_with',
        #  't': 'Organism',
        #  'label': 'correct',
        #  'triples': ['T001', 'T142', 'T001']}
        prompt = template.replace("{\"placeholder\": \"text_a\"}", data['text_a'])\
                         .replace("{\"placeholder\": \"text_b\"}", data['text_b'])\
                         .replace(" {\"mask\"} .", ": ")\
                         .replace(". This statement is", ".\nThis statement is")
        prompt = gpt3_template.replace("[TEMPLATE]", prompt)

        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=self.model_path,
            messages=messages,
            temperature=0,
            max_tokens=self.gpt_max_tokens
        )
        result = {"data": data, "prompt": prompt, "response": response}
        return result


class ChatGPTInferencer(GPT3Inferencer):
    def make_prediction(self, template, gpt3_template, data):
        # {'h': 'Organism',
        #  'r': 'interacts_with',
        #  't': 'Organism',
        #  'label': 'correct',
        #  'triples': ['T001', 'T142', 'T001']}
        prompt = template.replace("{\"placeholder\": \"text_a\"}", data['text_a']) \
                        .replace("{\"placeholder\": \"text_b\"}", data['text_b']) \
                        .replace(" {\"mask\"} .", ": ") \
                        .replace(". This statement is", ".\nThis statement is")
        prompt = gpt3_template.replace("[TEMPLATE]", prompt)

        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=self.model_path,
            messages=messages,
            temperature=0,
            max_tokens=self.gpt_max_tokens,
        )
        result = {"data": data, "prompt": prompt, "response": response}
        return result


class GPT3ZeroShotClassifier(GPT3Inferencer):
    def __init__(self, model_name, model_path, dataset, template, label_mapper, device):
        super().__init__(model_name, model_path, dataset, template, label_mapper, device)
        labels = ["This statement is true or right or correct", "this statement is false or wrong or incorrect"]
        self.label_embeddings = [get_embedding(label, engine=model_path) for label in labels]

    def make_prediction(self, template, gpt3_template, data):
        # {'h': 'Organism',
        #  'r': 'interacts_with',
        #  't': 'Organism',
        #  'label': 'correct',
        #  'triples': ['T001', 'T142', 'T001']}
        def label_score(statement_embedding, label_embeddings):
            return cosine_similarity(statement_embedding, label_embeddings[0]) - \
                  cosine_similarity(statement_embedding, label_embeddings[1])
        prompt = template.replace("{\"placeholder\": \"text_a\"}", data['text_a'])\
                         .replace("{\"placeholder\": \"text_b\"}", data['text_b'])\
                         .replace(" {\"mask\"} .", ": ")\
                         .replace(". This statement is", ".")

        prompt_embedding = get_embedding(prompt, engine=self.model_path)

        score = label_score(prompt_embedding, self.label_embeddings)
        predict = "correct" if score > 0 else "incorrect"
        result = {"data": data, "prompt": prompt, "response": predict}
        return result

class ZeroShotPromptClassifierFactory:

    def __new__(self, model_name):
        if model_name == "gpt3":
            return GPT3Inferencer
        elif model_name == "gpt3-ada":
            return GPT3ZeroShotClassifier
        elif model_name == 'gpt4':
            return GPT4Inferencer
        elif model_name == 'chatgpt':
            return ChatGPTInferencer
        else:
            return ZeroShotPromptClassifier
