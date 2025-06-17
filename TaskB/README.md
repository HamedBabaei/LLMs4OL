
**| [LLMs4OL Paradigm](../README.md#llms4ol-paradigm) | [Task A: Term Typing](../TaskA/README.md) | [Task B: Type Taxonomy Discovery](../TaskB/README.md) | [Task C: Type Non-Taxonomic Relation Extraction](../TaskC/README.md) | [Finetuning](../tuning/README.md) | [Task A Detailed Results](../TaskA/results/readme.md) | [Task B Detailed Results](../TaskB/results/readme.md) | [Task C Detailed Results](../TaskC/results/readme.md) | [Task A Datasets](../datasets/TaskA/README.md) | [Task B Datasets](../datasets/TaskB/README.md) | [Task C Datasets](../datasets/TaskC/README.md) | [Finetuning Datasets](../datasets/Tuning/README.md) |**

# Task B: Type Taxonomy Discovery

- **Task Definition**: For a given term types, identify the “is-a” hierarchies between them.
- **Task Goal**: A taxonomic hierarchy between pairs of types is discovered.
- **Evaluation Metric**: F1-Score


## Zero-Shot Testing

To run zero-shot testing you can try the following command line after you are done with [installing requirements](../README.md#requirements):

```bash
python3 test.py [-h] --kb_name KB_NAME --model MODEL --template TEMPLATE --device DEVICE
```

Where KB_NAME, MODEL, TEMPLATE, and DEVICE accept the following values:


**KB_NAME**:
> ```geonames, umls, schema```

**MODEL**: 
> ```bert_large, flan_t5_large, flan_t5_xl, bart_large, gpt3, bloom_1b7, bloom_3b, gpt2_large, gpt2_xl, gpt3_ada, llama_7b, chatgpt, gpt4```

**TEMPLATE**: All the templates based on the chosen dataset can be accessed in [this table](../README.md#experiments).
> ```"1", "2", "3", "4", "5", "6", "7", "8"```

**DEVICE:** 
> ```cpu, cuda```

As an example run if you want to run your model on the `geonames` dataset with the `bert_large` model on template `1` and I have GPU resource, the command line would be:

```bash
python3 test.py --kb_name="geonames" --model="bert_large" --template="1" --device="cuda"
```

Or you can easily run the `test_manual.sh` script:

```bash
./test_manual.sh
```
and It will ask you for the dataset and model name then it will run the model on all 8 prompt templates and then will save the results in the results directory. Since the number of runs will be very large, We have created `test_auto.sh` to run all the possible combinations with datasets, templates, and models.
```bash
./test_auto.sh
```
