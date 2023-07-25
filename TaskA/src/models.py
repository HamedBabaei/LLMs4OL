from transformers import AutoTokenizer, BertForMaskedLM, \
                         BartForConditionalGeneration, \
                         T5Tokenizer, T5ForConditionalGeneration, \
                         BloomForCausalLM, BloomTokenizerFast, \
                         LlamaForCausalLM
import torch
import openai
import time
from tqdm import tqdm

class BaseLM:

    def __init__(self, config) -> None:
        self.config = config
        self.tokenizer = None
        self.model = None
        self.device = self.config.device
        self.top_n = self.config.top_n
        pass

    def load(self):
        pass

    def make_batch_prediction(self, Xs: list):
        pass

    def batch_tokenize(self, Xs):
        inputs = self.tokenizer(Xs, return_tensors="pt", padding=True)
        inputs.to(self.device)
        return inputs

    def single_tokenize(self, X):
        inputs = self.tokenizer(X, return_tensors="pt")
        inputs.to(self.device)
        return inputs

    def output_cleaner(self, pred, **kwargs):
        return pred

    def predict(self, X: str):
        pass

class MaskedLM(BaseLM):
    def __init__(self, config) -> None:
        super().__init__(config)

    def load(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)
        self.model = BertForMaskedLM.from_pretrained(self.config.model_path)
        print(f"Loaded BertForMaskedLM from {self.config.model_path}")
        self.model.to(self.device)
        self.model.eval()

    def predict(self, X:str):
        inputs = self.single_tokenize(X)
        with torch.no_grad():
            token_logits = self.model(**inputs).logits
        token_logits = token_logits.cpu()
        inputs = inputs.to('cpu')
        mask_token_index = torch.where(inputs["input_ids"] == self.tokenizer.mask_token_id)[1]
        mask_token_logits = token_logits[0, mask_token_index, :]
        top_n_tokens = torch.topk(mask_token_logits, self.top_n, dim=1)
        predictions, logits = [], []
        for indice, logit in zip(top_n_tokens.indices[0].tolist(), top_n_tokens.values[0].tolist()):
            predictions.append(self.output_cleaner(self.tokenizer.decode([indice])))
            logits.append(logit)
        return predictions, logits

    def make_batch_prediction(self, Xs):
        inputs = self.batch_tokenize(Xs)
        with torch.no_grad():
            token_logits = self.model(**inputs).logits
        token_logits = token_logits.cpu()
        inputs = inputs.to('cpu')
        batch_predictions, batch_logits = [], []
        for index, _ in enumerate(token_logits):
            mask_token_index = torch.where(torch.tensor([list(inputs["input_ids"][index].numpy())]) == self.tokenizer.mask_token_id)[1]
            mask_token_logits = token_logits[index, mask_token_index, :]
            top_n_tokens = torch.topk(mask_token_logits, self.top_n, dim=1)
            predictions, logits = [], []
            for indice, logit in zip(top_n_tokens.indices[0].tolist(), top_n_tokens.values[0].tolist()):
                predictions.append(self.output_cleaner(self.tokenizer.decode([indice])))
                logits.append(logit)
            batch_predictions.append(predictions)
            batch_logits.append(logits)
        return batch_predictions, batch_logits

class BARTMaskedLM(MaskedLM):
    def __init__(self, config) -> None:
        super().__init__(config)

    def load(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)
        self.model = BartForConditionalGeneration.from_pretrained(self.config.model_path,
                                                                  forced_bos_token_id=0)
        self.model.to(self.device)
        self.model.eval()
        print(f"Loaded BartForConditionalGeneration from{self.config.model_path}")

    def output_cleaner(self, pred, **kwargs):
        return pred.strip()

class EncoderDecoderLM(BaseLM):
    def __init__(self, config) -> None:
        super().__init__(config)

    def predict(self, X: str):
        inputs = self.single_tokenize(X)
        with torch.no_grad():
            sequence_ids = self.model.generate(inputs.input_ids,
                                               num_beams=50,
                                               num_return_sequences=self.top_n,
                                               max_length=5)
        sequences = self.tokenizer.batch_decode(sequence_ids, skip_special_tokens=True)
        sequences = [self.output_cleaner(seq, prompt=X) for seq in sequences]
        logits = [0 for seq in sequences]
        return sequences, logits

    def make_batch_prediction(self, Xs):
        predictions, logits = [], []
        inputs = self.batch_tokenize(Xs)
        with torch.no_grad():
            sequence_ids = self.model.generate(input_ids=inputs["input_ids"],
                                               attention_mask=inputs["attention_mask"],
                                               max_new_tokens=5)
        sequences = self.tokenizer.batch_decode(sequence_ids.cpu(), skip_special_tokens=True,
                                                clean_up_tokenization_spaces=False)
        sequences_logist = [0 for _ in sequences]
        for index in range(0, len(Xs)):
            predictions.append(sequences[self.top_n * index:self.top_n * (index + 1)])
            logits.append(sequences_logist[self.top_n * index:self.top_n * (index + 1)])
        predictions = [[self.output_cleaner(predict, prompt=prompt) for predict in predicts]
                       for predicts, prompt in zip(predictions, Xs) ]
        return predictions, logits

    def make_single_batch_prediction(self, Xs):
        predictions, logits = [], []
        for X in Xs:
            predict, logit = self.predict(X)
            predictions.append(predict)
            logits.append(logit)
        return predictions, logits

class FlanT5EncoderDecoderLM(EncoderDecoderLM):
    def __init__(self, config) -> None:
        super().__init__(config)

    def load(self):
        self.tokenizer = T5Tokenizer.from_pretrained(self.config.model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(self.config.model_path, device_map="balanced")
        print(f"Loaded T5ForConditionalGeneration from {self.config.model_path}")
        # self.model.to(self.device)
        self.model.eval()

    def batch_tokenize(self, Xs):
        inputs = self.tokenizer(Xs,
                                return_tensors="pt",
                                truncation=True,
                                padding='max_length',
                                max_length=256)
        inputs.to(self.device)
        return inputs

    def output_cleaner(self, pred, **kwargs):
        return pred.replace("<pad>", "").replace("</s>", "").strip()

class BARTEncoderDecoderLM(EncoderDecoderLM):
    def __init__(self, config) -> None:
        super().__init__(config)

    def load(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)
        self.model = BartForConditionalGeneration.from_pretrained(self.config.model_path,
                                                                  forced_bos_token_id=0)
        print(f"Loaded BartForConditionalGeneration from {self.config.model_path}")
        self.model.to(self.device)
        self.model.eval()


class BLOOMDecoderLM(EncoderDecoderLM):
    def __init__(self, config) -> None:
        super().__init__(config)

    def load(self):
        self.tokenizer = BloomTokenizerFast.from_pretrained(self.config.model_path)
        self.model = BloomForCausalLM.from_pretrained(self.config.model_path, device_map="balanced")
        print(f"Loaded BloomForCausalLM from{self.config.model_path}")
        # self.model.to(self.device)
        self.model.eval()

    def output_cleaner(self, pred, **kwargs):
        pred = pred.replace(kwargs['prompt'], "")
        return pred.replace("<pad>", "").replace("</s>", "").strip()

class LLaMADecoderLM(EncoderDecoderLM):
    def __init__(self, config) -> None:
        super().__init__(config)

    def load(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = LlamaForCausalLM.from_pretrained(self.config.model_path,
                                                      load_in_8bit=False,
                                                      torch_dtype=torch.float16,
                                                      device_map="balanced")
        print(f"Loaded LLamaForCausalLM from{self.config.model_path}")
        # self.model.to(self.device)
        self.model.eval()

    def output_cleaner(self, pred, **kwargs):
        pred = pred.replace(kwargs['prompt'], "")
        return pred


class Left2RightOnlineLM(BaseLM):

    def __init__(self, config) -> None:
        super().__init__(config)

    def output_cleaner(self, pred):
        return pred.rstrip('\n').strip()

    def predict(self, X: str):
        response = openai.Completion.create(
            model=self.config.model_path,
            prompt=X,
            temperature=0.7,
            max_tokens=self.config.gpt3_max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response

    def check_all_is_done(self, results):
        for result in results:
            if result['check'] == False:
                return False
        return True

    def make_batch_prediction(self, Xs):
        results = []
        for index, data in enumerate(Xs['sample']):
            results.append({"check": False})

        assert self.check_all_is_done(results) == False

        while not self.check_all_is_done(results):
            for index, data in tqdm(enumerate(Xs['sample'])):
                if results[index]['check'] != True:
                    try:
                        response = self.predict(data)
                        results[index]['result'] = {"response": response, "sample": data, "label": Xs['label'][index]}
                        results[index]['check'] = True
                    except Exception as err:
                        print(f"UNexpected {err}, {type(err)}")
                        print("Going to sleep for 5 second!")
                        time.sleep(5)
        return results


class GPT4Left2RightOnlineLM(Left2RightOnlineLM):

    def predict(self, X: str):
        messages = [{"role": "user", "content": X}]
        response = openai.ChatCompletion.create(
            model=self.config.model_path,
            messages=messages,
            temperature=0,
            max_tokens=self.config.gpt4_max_tokens,
        )
        return response

class ChatGPTLeft2RightOnlineLM(Left2RightOnlineLM):

    def predict(self, X: str):
        messages = [{"role": "user", "content": X}]
        response = openai.ChatCompletion.create(
            model=self.config.model_path,
            messages=messages,
            temperature=0,
            max_tokens=self.config.chatgpt_max_tokens,
        )
        return response

class InferenceFactory:

    def __init__(self, config) -> None:
        self.models = {
            "bert_large": MaskedLM,
            "pubmed_bert": MaskedLM,
            "bart_large": BARTMaskedLM,
            "flan_t5_large": FlanT5EncoderDecoderLM,
            "flan_t5_xl": FlanT5EncoderDecoderLM,
            "bloom_1b7": BLOOMDecoderLM,
            "bloom_3b": BLOOMDecoderLM,
            "gpt3": Left2RightOnlineLM,
            "llama_7b": LLaMADecoderLM,
            "gpt4": GPT4Left2RightOnlineLM,
            "chatgpt": ChatGPTLeft2RightOnlineLM
        }
        self.config = config

    def __call__(self, model_name):
        try:
            model = self.models.get(model_name)(config=self.config)
        except ValueError:
            print("Oops! That was not valid model name. Try again ... ")
            exit(0)
        model.load()
        return model


