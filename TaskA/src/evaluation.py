import numpy as np

def precision_at_k(actual, predicted):
    act_set = set(actual)
    pred_set = set(predicted)
    result = len(act_set & pred_set) / float(len(predicted))
    return result*100

def apk(actual, predicted, k):
    """
    Computes the average precision at k.
    This function computes the average prescision at k between two lists of
    items.
    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The average precision at k over the input lists
    """
    if not actual:
        return 0.0
    if len(predicted)>k:
        predicted = predicted[:k]
    score = 0.0
    num_hits = 0.0
    for i,p in enumerate(predicted):
        # first condition checks whether it is valid prediction
        # second condition checks if prediction is not repeated
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)
    return score / min(len(actual), k)


def mapk(actual, predicted, k):
    """
    Computes the mean average precision at k.
    This function computes the mean average prescision at k between two lists
    of lists of items.
    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int,
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The mean average precision at k over the input lists
    """
    return np.mean([apk(a, p, k) for a,p in zip(actual, predicted)])


class EvaluationMetrics:

    def __init__(self, ks:list, metric="map") -> None:
        self.ks = ks
        self.metric=metric

    def evaluate(self, actual:list, predicted:list):
        if self.metric == "map":
            return self.MAP(actual, predicted)
        else:
            return self.AP(actual, predicted)

    def MAP(self, actual:list, predicted:list):
        results_dict = {}
        for k in self.ks:
            results_dict["MAP@"+str(k)] = mapk(actual=actual, predicted=predicted, k=k)
        return results_dict

    def AP(self, actual:list, predicted:list):
        results_dict = {}
        for k in self.ks:
            results_dict["AP@"+str(k)] = [apk(actual=actual, predicted=predicted, k=k)
                                          for a, p in zip(actual, predicted)]
        return results_dict
