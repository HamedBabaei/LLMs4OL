
**| [LLMs4OL Paradigm](../README.md#llms4ol-paradigm) | [Task A: Term Typing](../TaskA/README.md) | [Task B: Type Taxonomy Discovery](../TaskB/README.md) | [Task C: Type Non-Taxonomic Relation Extraction](../TaskC/README.md) | [Finetuning](../tuning/README.md) | [Task A Detailed Results](../TaskA/results/readme.md) | [Task B Detailed Results](../TaskB/results/readme.md) | [Task C Detailed Results](../TaskC/results/readme.md) | [Task A Datasets](../datasets/TaskA/README.md) | [Task B Datasets](../datasets/TaskB/README.md) | [Task C Datasets](../datasets/TaskC/README.md) | [Finetuning Datasets](../datasets/Tuning/README.md) |**

# Task C: Type Non-Taxonomic Relation Extraction

- **Task Definition**: For a given term types, identify and extract “non-is-a” or semantic relationships between types.
- **Task Goal**: To discover non-taxonomic semantic heterarchical relations between types.
- **Evaluation Metric**: F1-Score



## Zero-Shot Testing

To run zero-shot testing you can try the following command line after you are done with [installing requirements](../README.md#requirements):

```bash
python3 test.py [-h] --kb_name KB_NAME --model MODEL --device DEVICE
```

Where KB_NAME, MODEL, TEMPLATE, and DEVICE accept the following values:


**KB_NAME**:
> ```umls```

**MODEL**: 
> ```bert_large, flan_t5_large, flan_t5_xl, bart_large, gpt3, bloom_1b7, bloom_3b, llama_7b, chatgpt, gpt4```

**DEVICE:** 
> ```cpu, cuda```

As an example run if you want to run your model on the `umls` dataset with the `bert_large` model and I have GPU resource, the command line would be:

```bash
python3 test.py --kb_name="umls" --model="bert_large" --device="cuda"
```

Or you can easily run the `test_auto.sh` script to run models on `umls` dataset:

```bash
./test_auto.sh
```

