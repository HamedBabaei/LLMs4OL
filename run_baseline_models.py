from configuration import BaseConfig
from datahandler import DataReader, DataWriter
from src import WNDataset
from src import BaselineFactory
from torch.utils.data import DataLoader
from tqdm import tqdm
import argparse
from src import EvaluationFactory


def inference(model, dataloader):
    predictions, logits, labels = [], [], []
    for batch in tqdm(dataloader):
        prediction, logit = model.make_batch_prediction(list(batch['sample']))
        for pred, log, label in zip(prediction, logit, list(batch['label'])):
            predictions.append(pred)
            logits.append(list(log))
            labels.append(label)
    return predictions, logits, labels

if __name__=="__main__":
        
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_name", required=True)
    parser.add_argument("--model_name", required=True)
    parser.add_argument("--template", required=True)
    args = parser.parse_args()
   
    print("args:", args)
    config = BaseConfig(version=2).get_args(db_name=args.db_name, model=args.model_name, template=args.template)

    dataset = DataReader.load_json(config.entity_path)

    test_dataset = WNDataset(data=dataset, dataset_type='test', template=args.template, is_train=False)
    report_dict = {
        "baseline-run-args": str(args),
        "report_output_refrence": config.report_output,
        "results":[],
        "dataset-in-use": str(test_dataset),
        "configs": vars(config),
        "dataset-stats": dataset['stats']
    }
    test_dataloader = DataLoader(test_dataset, batch_size=config.batch_size, shuffle=False, collate_fn=test_dataset.collate_fn)

    baseline_model = BaselineFactory(config)(model_name=args.model_name) 
    predictions, logits, labels = inference(model=baseline_model, dataloader=test_dataloader)
    outputs = {
        "model-name":args.model_name, 
        "dataset":report_dict['dataset-in-use'], 
        "predictions":predictions, 
        "logits":logits, 
        "labels":labels
    }
    DataWriter.write_json(outputs,  config.model_output)
    print(f"scoring model outputs in:{config.model_output}")

    evaluator = EvaluationFactory()(metric_name="mp")
    results = evaluator.evaluate(actuals=labels, predictions=predictions)
    report_dict['results'] = results
    print("Results:", results)
    print(f"scoring results in:{config.report_output}")
    DataWriter.write_json(report_dict,  config.report_output)


