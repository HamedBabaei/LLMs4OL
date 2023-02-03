from transformers import AutoTokenizer, BertForMaskedLM
import torch


class Baseline:

    def __init__(self, config) -> None:
        self.config = config
        pass
    
    def fit(self, X, Y):
        pass

    def make_batch_prediction(self, Xs:list):
        pass

    def predict(self, X:str):
        pass


class BERTLarge(Baseline):

    def __init__(self, config) -> None:
        super().__init__(config)
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)
        self.model = BertForMaskedLM.from_pretrained(self.config.model_path)
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
            predictions.append(self.tokenizer.decode([indice]))
            logits.append(logit)
        return predictions, logits

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
                predictions.append(self.tokenizer.decode([indice]))
                logits.append(logit)
            batch_predictions.append(predictions)
            batch_logits.append(logits)
        return batch_predictions, batch_logits

    
class NgramLM(Baseline):
    def __init__(self, config) -> None:
        super().__init__(config)
    
    def fit(self, X, Y):
        pass
    
    def make_batch_prediction(self, Xs):
        pass

    def predict(self, X):
        pass


class BaselineFactory:

    def __init__(self, config) -> None:
        self.models = {
            "bert_large": BERTLarge
        }
        self.config = config
    
    def __call__(self, model_name):
        return self.models[model_name](config=self.config)
        

