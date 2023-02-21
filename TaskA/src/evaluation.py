

def precision_at_k(actual, predicted):
    act_set = set(actual)
    pred_set = set(predicted)
    result = len(act_set & pred_set) / float(len(predicted))
    return result*100

def recall_at_k(actual, predicted):
    act_set = set(actual)
    pred_set = set(predicted)
    result = len(act_set & pred_set) / float(len(act_set))
    return result*100


class Evaluation:

    def __init__(self) -> None:
        pass

    def evaluate(self, actuals:list, predictions:list):
        scores = []
        for actual, prediction in zip(actuals, predictions):
            scores.append(self._evaluate(actual=actual, prediction=prediction))
        return self._results(scores)

    def _evaluate(self, actual:list, prediction:list) -> list:
        pass

    def _results(self, scores) -> dict:
        pass


class MP(Evaluation):

    def __init__(self) -> None:
        super().__init__()

    def _evaluate(self, actual: list, prediction: list) -> list:
        precision_at_1 = precision_at_k(actual=actual, predicted=prediction[:1])
        precision_at_5 = precision_at_k(actual=actual, predicted=prediction[:5])
        precision_at_10 = precision_at_k(actual=actual, predicted=prediction[:10])
        
        recall_at_1 = recall_at_k(actual=actual, predicted=prediction[:1])
        recall_at_5 = recall_at_k(actual=actual, predicted=prediction[:5])
        recall_at_10 = recall_at_k(actual=actual, predicted=prediction[:10])

        return [precision_at_1, precision_at_5, precision_at_10, recall_at_1, recall_at_5, recall_at_10]

    def _results(self, scores: list) -> dict:
        mp_at_1 = sum([score[0] for score in scores])/len(scores)
        mp_at_5 = sum([score[1] for score in scores])/len(scores)
        mp_at_10 = sum([score[2] for score in scores])/len(scores)
        
        mr_at_1 = sum([score[3] for score in scores])/len(scores)
        mr_at_5 = sum([score[4] for score in scores])/len(scores)
        mr_at_10 = sum([score[5] for score in scores])/len(scores)

        return {"P@1": mp_at_1, "P@5": mp_at_5, "P@10": mp_at_10, 
                "R@1": mr_at_1, "R@5": mr_at_5, "R@10": mr_at_10}


class EvaluationFactory:

    def __init__(self) -> None:
        self.metrics = {
            "mp":MP
        }

    def __call__(self, metric_name):
        return self.metrics[metric_name]()
        