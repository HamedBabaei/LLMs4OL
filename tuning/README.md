
**| [LLMs4OL Paradigm](../README.md#llms4ol-paradigm) | [Task A: Term Typing](../TaskA/README.md) | [Task B: Type Taxonomy Discovery](../TaskB/README.md) | [Task C: Type Non-Taxonomic Relation Extraction](../TaskC/README.md) | [Finetuning](../tuning/README.md) | [Task A Detailed Results](../TaskA/results/readme.md) | [Task B Detailed Results](../TaskB/results/readme.md) | [Task C Detailed Results](../TaskC/results/readme.md) | [Task A Datasets](../datasets/TaskA/README.md) | [Task B Datasets](../datasets/TaskB/README.md) | [Task C Datasets](../datasets/TaskC/README.md) | [Finetuning Datasets](../datasets/Tuning/README.md) |**

# Few-Shot Learning

- **Task Definition**: Train a single model per source to perform term typing, type taxonomy discovery, and type non-taxonomic relation extraction.
- **Task Goal**: Leverage LLMs for ontology learning.
- **Evaluation Approach**: Zero-shot testing
- **Number of samples per class**: 8 sample per-class

## Training

To run few-shot training you can try the following command line after you are done with [installing requirements](../README.md#requirements):

```bash
python3 trainer.py [-h] --kb_name KB_NAME --model_to_train MODEL_TO_TRAIN [--num_train_epochs NUM_TRAIN_EPOCHS]
```

Where NUM_TRAIN_EPOCHS is an optional argument and the default is set to `15`. But KB_NAME and MODEL_TO_TRAIN arguments accept the following values:

**KB_NAME**:
> ```wn18rr, geonames, umls, schemaorg```

**MODEL_TO_TRAIN**: 
> ```flan_t5_large, flan_t5_xl```

As an example run if you want to train your model on the `wn18rr` dataset with the `flan_t5_large`, the command line would be:

```bash
python3 trainer.py --kb_name="wn18rr" --model_name="flan_t5_large"
```
In the end, you can expect the following artifacts to be created in the `../assets/Tuning/wn18rr-flan-t5-large` directory. As a result of this, we can obtain the following models by using `trainer`:

> `wn18rr_flan_t5_large`, `wn18rr_flan_t5_xl`, `geonames_flan_t5_large`, `geonames_flan_t5_xl`, `umls_flan_t5_large`, `umls_flan_t5_xl`, `schemaorg_flan_t5_large`, `schemaorg_flan_t5_xl`

## Testing

The same `test.py` scripts in task A, B, and C will be used with the same arguments for testing but with the obtained models.

## All in One
To make life easier, to train and evaluate models you can just run the following shell script. It will automatically train and evaluate models on datasets.
```bash
./train_eval.sh
```
---- 

**Notes:**
- The training requires GPU resources.
