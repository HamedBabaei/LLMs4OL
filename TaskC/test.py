from configuration import BaseConfig
from datahandler import DataReader, DataWriter
import argparse
import datetime
from src import ZeroShotPromptClassifierFactory, EvaluationMetrics
import openai_key_setter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb_name", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--device", required=True)
    args = parser.parse_args()

    print("args:", args)
    config = BaseConfig().get_args(kb_name=args.kb_name, model=args.model)
    start_time = datetime.datetime.now()
    print("Starting the Inference time is:", str(start_time).split('.')[0])
    dataset = DataReader.load_json(config.processed_sn)
    templates = DataReader.load_text(config.template_text).split("\n")
    template = templates[config.template]
    print(f"Working on template: {config.template}: {template}")
    label_mapper = DataReader.load_json(config.labels_path)

    zero_shot_prompt_classifier = ZeroShotPromptClassifierFactory(model_name = config.model_name)

    model = zero_shot_prompt_classifier(model_name=config.model_name,
                                         model_path=config.model_path,
                                         dataset=dataset,
                                         template=template,
                                         label_mapper=label_mapper,
                                         device=args.device)


    if config.model_name == "gpt3":
        results = model.test()
        print(f"output predictions in :{config.model_output}")
        DataWriter.write_json(results, config.model_output)
    else:
        y_true, y_pred  = model.test()
        results = EvaluationMetrics.evaluate(actual=y_true, predicted=y_pred)
        print(results['clf-report'])
        report_dict = {
            "baseline-run-args": str(args),
            "report_output_refrence": config.report_output,
            "results": results,
            "dataset-in-use": str(args.kb_name),
            "configs": vars(config)
        }

        print(f"scoring results in:{config.report_output}")
        DataWriter.write_json(report_dict, config.report_output)
        end_time = datetime.datetime.now()
        print("Ending the Inference time is:", str(end_time).split('.')[0])
        print("Total duration is===>", str(end_time - start_time))