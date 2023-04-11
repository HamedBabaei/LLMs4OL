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

    outputs_file = []
    for file in os.listdir(output_dir):
        if "output" in file and config.template in file:
            outputs_file.append(file)
    assert len(outputs_file) == 1

    output_file_path = os.path.join(output_dir, outputs_file[0])
    report_file_path = os.path.join(output_dir, f"report-{config.model}-{outputs_file[0].split(f'-{config.model}-')[1]}")

    print("scoring model outputs in:", output_file_path)
    outputs = DataReader.load_json(output_file_path)

    if config.model in config.models_with_special_output:
        predictions, labels = [], []
        for output in outputs:
            label = output['result']['data']['label']
            if "ada" in config.model:
                predict = output['result']['response']
            else:
                predict = output['result']['response']['choices'][0]['text'].lower().rstrip('\n').strip()
                predict = "correct" if "true" in predict else "incorrect"
            predictions.append(predict)
            labels.append(label)
    else:
        predictions = outputs['predictions']
        labels = outputs['labels']
    results = EvaluationMetrics.evaluate(actual=labels, predicted=predictions)
    report = {
            "report_output_refrence": report_file_path,
            "results": results,
            "dataset-in-use": str(config.kb_name),
            "configs": vars(config)
    }


    print("Results:", report['results']['clf-report'])
    print("storing results in:", report_file_path)
    DataWriter.write_json(data=report, path=report_file_path)
