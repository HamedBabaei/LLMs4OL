from configuration import BaseConfig
from datahandler import DataReader, DataWriter
from src import InferenceDatasetFactory
from src import InferenceFactory
from torch.utils.data import DataLoader
from tqdm import tqdm
import argparse
from src import EvaluationMetrics


def inference(model, dataloader):
    predictions, logits, labels = [], [], []
    for batch in tqdm(dataloader):
        prediction, logit = model.make_batch_prediction(list(batch['sample']))
        for pred, log, label in zip(prediction, logit, list(batch['label'])):
            predictions.append(pred)
            logits.append(list(log))
            labels.append(label)
    return predictions, logits, labels


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb_name", required=True)
    parser.add_argument("--model_name", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--device", required=True)
    args = parser.parse_args()
   
    print("args:", args)
    config = BaseConfig(version=3).get_args(kb_name=args.kb_name, model=args.model_name, template=args.template)

    dataset = DataReader.load_json(config.entity_path)
    templates = DataReader.load_json(config.templates_json)[config.template_name]

    test_dataset = InferenceDatasetFactory(kb_name=args.kb_name, data=dataset, templates=templates, template=args.template)

    report_dict = {
        "baseline-run-args": str(args),
        "report_output_refrence": config.report_output,
        "results":[],
        "dataset-in-use": str(test_dataset),
        "configs": vars(config)
    }
    test_dataloader = DataLoader(test_dataset, batch_size=config.batch_size, shuffle=False, collate_fn=test_dataset.collate_fn)

    inference_model = InferenceFactory(config)(model_name=args.model_name) 
    predictions, logits, labels = inference(model=inference_model, dataloader=test_dataloader)
    outputs = {
        "model-name": args.model_name,
        "dataset": report_dict['dataset-in-use'],
        "predictions": predictions,
        "logits": logits,
        "labels": labels
    }
    DataWriter.write_json(outputs,  config.model_output)
    print(f"scoring model outputs in:{config.model_output}")

    evaluator = EvaluationMetrics(ks=config.eval_ks, metric=config.eval_metric)
    results = evaluator.evaluate(actual=labels, predicted=predictions)
    report_dict['results'] = results
    print("Results:", results)
    print(f"scoring results in:{config.report_output}")
    DataWriter.write_json(report_dict,  config.report_output)


