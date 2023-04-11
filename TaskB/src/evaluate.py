from sklearn.metrics import accuracy_score, f1_score, \
                            classification_report

class EvaluationMetrics:

    def __int__(self):
        pass

    @staticmethod
    def evaluate(actual, predicted):
        # f1 = f1_score(actual, predicted)
        accuracy = accuracy_score(actual, predicted)
        clf_report = classification_report(actual, predicted)
        clf_report_dict = classification_report(actual, predicted, output_dict=True)
        return {"accuracy": accuracy, "clf-report": clf_report, "clf-report-dict":clf_report_dict}


