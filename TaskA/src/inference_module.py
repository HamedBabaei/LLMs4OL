from transformers import AutoTokenizer, BertForMaskedLM
from transformers import BartForConditionalGeneration
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import openai
import time
class BaseLM:

    def __init__(self, config) -> None:
        self.config = config
        pass
    
    def fit(self, X, Y):
        pass

    def make_batch_prediction(self, Xs:list):
        pass

    def predict(self, X:str):
        pass


class MaskedLM(BaseLM):

    def __init__(self, config) -> None:
        super().__init__(config)
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)
        self.model_name = config.template_name
        if self.model_name == "bart":
            self.model = BartForConditionalGeneration.from_pretrained(self.config.model_path,
                                                                      forced_bos_token_id=0)
            print(f"Loaded BartForConditionalGeneration from{self.config.model_path}")
        else:
            self.model = BertForMaskedLM.from_pretrained(self.config.model_path)
            print(f"Loaded BertForMaskedLM from {self.config.model_path}")

        self.device = self.config.device
        self.model.to(self.device)
        self.top_n = self.config.top_n
        
    def predict(self, X:str):        
        inputs = self.tokenizer(X, return_tensors="pt")
        inputs.to(self.device)
        with torch.no_grad():
            token_logits = self.model(**inputs).logits
        token_logits = token_logits.cpu()
        inputs = inputs.to('cpu')
        mask_token_index = torch.where(inputs["input_ids"] == self.tokenizer.mask_token_id)[1]
        mask_token_logits = token_logits[0, mask_token_index, :]
        top_n_tokens = torch.topk(mask_token_logits, self.top_n, dim=1)
        predictions, logits = [], []
        for indice, logit in zip(top_n_tokens.indices[0].tolist(), top_n_tokens.values[0].tolist()):
            if self.model_name=='bart':
                predictions.append(self.__output_cleaner(self.tokenizer.decode([indice])))
            else:
                predictions.append(self.tokenizer.decode([indice]))
            logits.append(logit)
        return predictions, logits

    def __output_cleaner(self, pred):
        return pred.strip()

    def make_batch_prediction(self, Xs):
        inputs = self.tokenizer(Xs, return_tensors="pt", padding=True)
        inputs.to(self.device)
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
                if self.model_name == 'bart':
                    predictions.append(self.__output_cleaner(self.tokenizer.decode([indice])))
                else:
                    predictions.append(self.tokenizer.decode([indice]))
                logits.append(logit)
            batch_predictions.append(predictions)
            batch_logits.append(logits)
        return batch_predictions, batch_logits


class EncoderDecoderLM(BaseLM):

    def __init__(self, config) -> None:
        super().__init__(config)
        self.model_name = config.template_name
        if self.model_name == "bart":
            self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)
            self.model = BartForConditionalGeneration.from_pretrained(self.config.model_path,
                                                                      forced_bos_token_id=0)
            print(f"Loaded BartForConditionalGeneration from{self.config.model_path}")
        else:
            self.tokenizer = T5Tokenizer.from_pretrained(self.config.model_path)
            self.model = T5ForConditionalGeneration.from_pretrained(self.config.model_path)
            print(f"Loaded T5ForConditionalGeneration from {self.config.model_path}")
        self.device = self.config.device
        self.model.to(self.device)
        self.top_n = self.config.top_n

    def __output_cleaner(self, pred):
        return pred.replace("<pad>", "").replace("</s>","").strip()

    def predict(self, X:str):
        inputs = self.tokenizer(X, return_tensors="pt")
        inputs.to(self.device)
        with torch.no_grad():
            sequence_ids = self.model.generate(inputs.input_ids, num_beams=200, num_return_sequences=self.top_n, max_length=5)
        sequences = self.tokenizer.batch_decode(sequence_ids, skip_special_tokens=True)
        sequences = [self.__output_cleaner(seq) for seq in sequences]
        logits = [0 for seq in sequences]
        return sequences, logits

    def make_batch_prediction(self, Xs):
        predictions, logits = [], []
        for X in Xs:
            predict, logit = self.predict(X)
            predictions.append(predict)
            logits.append(logit)
        return predictions, logits


class Left2RightOnlineLM(BaseLM):

    def __init__(self, config) -> None:
        super().__init__(config)
        self.model_name = config.template_name
        openai.api_key = config.openai_key


    def __output_cleaner(self, pred):
        return pred.rstrip('\n').strip()

    def predict(self, X:str):
        response = openai.Completion.create(
                  model=self.config.model_path,
                  prompt=X,
                  temperature=0.7,
                  max_tokens=10,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0
                )
        sequences = [self.__output_cleaner(response.choices[0].text)]
        logits = [0]

        return sequences, logits

    def make_batch_prediction(self, Xs):
        time.sleep(65)
        predictions, logits = [], []
        for X in Xs:
            predict, logit = self.predict(X)
            predictions.append(predict)
            logits.append(logit)
        return predictions, logits


class InferenceFactory:

    def __init__(self, config) -> None:
        self.models = {
            "bert_large": MaskedLM,
            "flan_t5_large": EncoderDecoderLM,
            "flan_t5_xl": EncoderDecoderLM,
            "bart_large": EncoderDecoderLM,
            "gpt3_babbage": Left2RightOnlineLM
        }
        self.config = config
    
    def __call__(self, model_name):
        return self.models[model_name](config=self.config)
        
