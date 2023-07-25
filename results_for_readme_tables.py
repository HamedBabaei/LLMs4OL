import json
import os
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import plotly.io as pio

pio.kaleido.scope.mathjax = None

model2name = {
    'bert_large': 'BERT-Large',
    'pubmed_bert': 'PubMedBERT',
    'bart_large': 'BART-Large',
    'flan_t5_large': 'Flan-T5-Large',
    'bloom_1b7': 'BLOOM-1b7',
    'flan_t5_xl': 'Flan-T5-XL',
    'bloom_3b': 'BLOOM-3b',
    'llama_7b': 'LLaMA-7B',
    'gpt3': 'GPT-3',
    'chatgpt': 'GPT-3.5',
    'gpt4': 'GPT-4',
    'umls_flan_t5_large': '`Flan-T5-Large*`',
    'umls_flan_t5_xl': '`Flan-T5-XL*`',
    'schemaorg_flan_t5_large': '`Flan-T5-Large*`',
    'schemaorg_flan_t5_xl': '`Flan-T5-XL*`',
    'geonames_flan_t5_large': '`Flan-T5-Large*`',
    'geonames_flan_t5_xl': '`Flan-T5-XL*`',
    'wn18rr_flan_t5_large': '`Flan-T5-Large*`',
    'wn18rr_flan_t5_xl': '`Flan-T5-XL*`',
}
llm_no = 13

dir2name = {
    'wn18rr': 'WN18RR',
    'geonames': 'GeoNames',
    'nci': 'NCI',
    'snomedct_us': 'SNOMEDCT_US',
    'medcin': 'Medcin',
    'umls': 'UMLS',
    'schema': 'Schema.Org'
}

medical_dir2name = {
    'nci': 'NCI',
    'snomedct_us': 'SNOMEDCT',
    'medcin': 'Medcin',
    'umls': 'UMLS',
}
tasks = ['A', 'B']

task_templates_name = {
    "A": [f'template-{str(index)}' for index in range(1, 9)],
    "B": [f'-{str(index)}-' for index in range(0, 8)],
    "C": [""]
}


def read_json(path: str):
    """
    Reads the ``json`` file of the given ``input_path``.

    :param input_path: Path to the json file
    :return: A loaded json object.
    """
    with open(path, encoding="utf-8") as f:
        json_data = json.load(f)
    return json_data


def make_string(score):
    str_score = str(score)
    return str_score.split(".")[0] + "." + str_score.split(".")[1][:3]


report_catalog = {}
for task in tasks:
    report_catalog[task] = {}
    root_task_dir = f"Task{task}/results/"
    for dataset in dir2name.keys():
        if dataset in os.listdir(root_task_dir):
            report_catalog[task][dataset] = {}
            # print(dir2name[dataset])
            dataset_dir_path = os.path.join(root_task_dir, dataset)
            for model_output_dir in os.listdir(dataset_dir_path):
                model_output_dir_path = os.path.join(dataset_dir_path, model_output_dir)
                if os.path.isdir(model_output_dir_path) and not '.ipynb_checkpoints' in model_output_dir_path:
                    prefix = f"report-{model_output_dir}"
                    results = []
                    for template in task_templates_name[task]:
                        finded = False
                        for file in os.listdir(model_output_dir_path):
                            if file.startswith(prefix) and template in file:
                                json_file = read_json(path=os.path.join(model_output_dir_path, file))
                                if task == 'A':
                                    score = make_string(json_file['results']['MAP@1'] * 100)
                                    results.append(score)
                                    finded = True
                                elif task == 'B':
                                    score = make_string(
                                        json_file['results']['clf-report-dict']['macro avg']['f1-score'] * 100)
                                    results.append(score)
                                    finded = True
                                elif task == 'C':
                                    score = make_string(
                                        json_file['results']['clf-report']['macro avg']['f1-score'] * 100)
                                    results.append(score)
                                    finded = True
                                break
                        if not finded:
                            results.append("-")
                    report_catalog[task][dataset][model_output_dir] = results


task = 'A'
reports = report_catalog[task]
print(task)
for source, results in reports.items():
    print("|", dir2name[source], end="|")
    for llm in list(model2name.values()):
        if llm == "`Flan-T5-XL*`":
            print(llm, end="|")
            break
        else:
            print(llm, end="<br>")
    res_str = "|"
    for index, template in enumerate(task_templates_name[task]):
        for llm_model, llm_name in model2name.items():
            if llm_name == "`Flan-T5-XL*`":
                if llm_model in list(results.keys()):
                    print(results[llm_model][index], end="|")
                    break
            else:
                if llm_model in list(results.keys()):
                    print(results[llm_model][index], end="<br>")
                else:
                    if llm_name == 'PubMedBERT':
                        print("-", end="<br>")
    print()
    print()


task = 'B'
reports = report_catalog[task]
print(task)
for source, results in reports.items():
    print("|", dir2name[source], end="|")
    for llm in list(model2name.values()):
        if llm == "`Flan-T5-XL*`":
            print(llm, end="|")
            break
        else:
            print(llm, end="<br>")
    res_str = "|"
    for index, template in enumerate(task_templates_name[task]):
        for llm_model, llm_name in model2name.items():
            if llm_name == "`Flan-T5-XL*`":
                if llm_model in list(results.keys()):
                    print(results[llm_model][index], end="|")
                    break
            else:
                if llm_model in list(results.keys()):
                    print(results[llm_model][index], end="<br>")
                else:
                    if llm_name == 'PubMedBERT':
                        print("-", end="<br>")
    print()
    print()

task = 'B'
reports = report_catalog[task]
print(task)
for source, results in reports.items():
    print(dir2name[source])
    for llm_model, llm_name in model2name.items():
        if llm_name.startswith("`Flan-T5-"):
            if llm_model in list(results.keys()):
                print("  &  ", llm_name, "  &  ", "  &  ".join([s[:-1] for s in results[llm_model]]), "\\\\")
        else:
            if llm_model in list(results.keys()):
                print("  &  ", llm_name, "  &  ", "  &  ".join([s[:-1] for s in results[llm_model]]), "\\\\")
            else:
                print("  &  ", llm_name, "  &  ", "  &  ".join([str("-") for _ in range(8)]), "\\\\")
    print()
    print()

task = 'A'
reports = report_catalog[task]
print(task)
for source, results in reports.items():
    print(dir2name[source])
    for llm_model, llm_name in model2name.items():
        if llm_name.startswith("`Flan-T5-"):
            if llm_model in list(results.keys()):
                print("  &  \\textit{", llm_name[1:][:-2], "$^*$}  &  ",
                      "  &  ".join([s[:-1] if len(s) > 1 else s for s in results[llm_model]]), "\\\\")
                # break
        else:
            if llm_model in list(results.keys()):
                print("  &  ", llm_name, "  &  ",
                      "  &  ".join([s[:-1] if len(s) > 1 else s for s in results[llm_model]]), "\\\\")
            else:
                print("  &  ", llm_name, "  &  ", "  &  ".join([str("-") for _ in range(8)]), "\\\\")

    print()
    print()
