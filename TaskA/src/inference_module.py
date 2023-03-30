from transformers import AutoTokenizer, BertForMaskedLM
from transformers import BartForConditionalGeneration
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import openai
import time
from tqdm import tqdm

class BaseLM:

    def __init__(self, config) -> None:
        self.config = config
        pass

    def fit(self, X, Y):
        pass

    def make_batch_prediction(self, Xs: list):
        pass

    def predict(self, X: str):
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
        self.model.eval()
        self.top_n = self.config.top_n

    def __output_cleaner(self, pred):
        return pred.replace("<pad>", "").replace("</s>", "").strip()

    def predict(self, X: str):
        inputs = self.tokenizer(X, return_tensors="pt")
        inputs.to(self.device)
        with torch.no_grad():
            sequence_ids = self.model.generate(inputs.input_ids, num_beams=50, num_return_sequences=self.top_n,
                                               max_length=5)
        sequences = self.tokenizer.batch_decode(sequence_ids, skip_special_tokens=True)
        sequences = [self.__output_cleaner(seq) for seq in sequences]
        logits = [0 for seq in sequences]
        return sequences, logits

    def make_batch_prediction(self, Xs):
        predictions, logits = [], []
        # inputs = self.tokenizer(Xs, return_tensors="pt", truncation=True, padding='max_length', max_length=256)
        inputs = self.tokenizer(Xs, return_tensors="pt",padding=True)
        inputs.to(self.device)
        with torch.no_grad():
            sequence_ids = self.model.generate(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"],
                                               num_beams=50, num_return_sequences=self.top_n, max_length=5)
        sequences = self.tokenizer.batch_decode(sequence_ids.cpu(), skip_special_tokens=True,
                                                clean_up_tokenization_spaces=False)
        sequences = [self.__output_cleaner(seq) for seq in sequences]
        sequences_logist = [0 for _ in sequences]
        for index in range(0, len(Xs)):
            predictions.append(sequences[self.top_n * index:self.top_n * (index + 1)])
            logits.append(sequences_logist[self.top_n * index:self.top_n * (index + 1)])
        return predictions, logits

    def make_single_batch_prediction(self, Xs):
        predictions, logits = [], []
        for X in Xs:
            predict, logit = self.predict(X)
            predictions.append(predict)
            logits.append(logit)
        return predictions, logits


class EncoderDecoderLMMultiGPU(BaseLM):

    def __init__(self, config) -> None:
        super().__init__(config)
        self.model_name = config.template_name
        self.tokenizer = T5Tokenizer.from_pretrained(self.config.model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(self.config.model_path, device_map="balanced")
        print(f"Loaded T5ForConditionalGeneration from {self.config.model_path}")
        self.model.eval()
        self.device = config.device
        self.top_n = self.config.top_n

    def __output_cleaner(self, pred):
        return pred.replace("<pad>", "").replace("</s>", "").strip()

    def predict(self, X: str):
        inputs = self.tokenizer(X, return_tensors="pt")
        inputs.to(self.device)
        with torch.no_grad():
            sequence_ids = self.model.generate(inputs.input_ids, num_beams=200, num_return_sequences=self.top_n,
                                               max_length=5)
        sequences = self.tokenizer.batch_decode(sequence_ids, skip_special_tokens=True)
        sequences = [self.__output_cleaner(seq) for seq in sequences]
        logits = [0 for seq in sequences]
        return sequences, logits

    def make_batch_prediction(self, Xs):
        predictions, logits = [], []
        inputs = self.tokenizer(Xs, return_tensors="pt", truncation=True, padding='max_length', max_length=256)
        # inputs = self.tokenizer(Xs, return_tensors="pt", padding=True)
        inputs.to(self.device)
        with torch.no_grad():
            sequence_ids = self.model.generate(inputs.input_ids, max_length=5)
            # sequence_ids = self.model.generate(inputs.input_ids, num_beams=50, num_return_sequences=self.top_n, max_length=5)
        sequences = self.tokenizer.batch_decode(sequence_ids, skip_special_tokens=True,
                                                clean_up_tokenization_spaces=False)
        sequences = [self.__output_cleaner(seq) for seq in sequences]
        sequences_logist = [0 for _ in sequences]
        for index in range(0, len(Xs)):
            predictions.append(sequences[self.top_n * index:self.top_n * (index + 1)])
            logits.append(sequences_logist[self.top_n * index:self.top_n * (index + 1)])
        return predictions, logits

class Left2RightOnlineLM(BaseLM):

    def __init__(self, config) -> None:
        super().__init__(config)
        self.model_name = config.template_name

    def __output_cleaner(self, pred):
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


class InferenceFactory:

    def __init__(self, config) -> None:
        self.models = {
            "bert_large": MaskedLM,
            "flan_t5_large": EncoderDecoderLM,
            "flan_t5_xl": EncoderDecoderLM,
            "bart_large": MaskedLM,
            "gpt3": Left2RightOnlineLM
        }
        self.config = config
        if self.config.multi_gpu:
            self.models['flan_t5_large'] = EncoderDecoderLMMultiGPU
            self.models['flan_t5_xl'] = EncoderDecoderLMMultiGPU

    def __call__(self, model_name):
        return self.models[model_name](config=self.config)

