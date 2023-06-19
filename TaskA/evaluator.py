from configuration import ExternalEvaluationConfig
from datahandler import DataReader, DataWriter
import os
from src import EvaluationMetrics


if __name__=="__main__":
    config = ExternalEvaluationConfig().get_args()
    output_dir = os.path.join(config.root_dir, config.kb_name, config.model)

    if not os.path.exists(output_dir):
        print(f"'{output_dir}' is not existed!")
        exit(0)

    reports_file, outputs_file = [], []
    for file in os.listdir(output_dir):
        if 'report' in file and config.template in file:
            reports_file.append(file)
        elif "output" in file and config.template in file:
            outputs_file.append(file)
    assert len(reports_file) == 1
    assert len(outputs_file) != 0

    outputs = []
    if "gpt" in config.model:
        for file in outputs_file:
            output_file_path = os.path.join(output_dir, file)
            print("scoring model outputs in:", output_file_path)
            outputs += DataReader.load_json(output_file_path)
    else:
        output_file_path = os.path.join(output_dir, outputs_file[0])
        print("scoring model outputs in:", output_file_path)
        outputs = DataReader.load_json(output_file_path)['outputs']

    report_file_path = os.path.join(output_dir, reports_file[0])
    report = DataReader.load_json(report_file_path)
    if len(report['results']) == 0 or "bloom" in config.model or "flan" in config.model or "llama" in config.model:
        if config.model == "gpt3":
            predictions, labels = [], []
            for output in outputs:
                label_list = output['result']['label']
                predict = output['result']['response']['choices'][0]['text'].lower().rstrip('\n').strip()
                predict_list = []
                for label in label_list:
                    if label.lower() in predict:
                        predict_list.append(label)
                predictions.append(predict_list)
                labels.append(label_list)
        elif config.model == "gpt4" or config.model=='chatgpt':
            predictions, labels = [], []
            for output in outputs:
                label_list = output['result']['label']
                predict = output['result']['response']['choices'][0]['message']['content'].lower().rstrip('\n').strip()
                predict_list = []
                for label in label_list:
                    if label.lower() in predict:
                        predict_list.append(label)
                predictions.append(predict_list)
                labels.append(label_list)
        elif "bloom" in config.model or "flan" in config.model or "llama" in config.model:
            predictions, labels = [], []
            for output in outputs:
                label_list = output['label']
                predict = output['pred'][0].lower().rstrip('\n').strip()
                predict_list = []
                for label in label_list:
                    if label.lower() in predict or predict in label.lower():
                        predict_list.append(label)
                predictions.append(predict_list)
                labels.append(label_list)
        else:
            predictions = outputs['predictions']
            labels = outputs['labels']
        evaluator = EvaluationMetrics(ks=config.eval_ks, metric=config.eval_metric)
        results = evaluator.evaluate(actual=labels, predicted=predictions)
        report['results'] = results
        DataWriter.write_json(data=report, path=report_file_path)

    print("Results:", report['results'])
    print("storing results in:", os.path.join(output_dir, reports_file[0]))

