
**| [LLMs4OL Paradigm](../../README.md#llms4ol-paradigm) | [Task A: Term Typing](../../TaskA/README.md) | [Task B: Type Taxonomy Discovery](../../TaskB/README.md) | [Task C: Type Non-Taxonomic Relation Extraction](../../TaskC/README.md) | [Finetuning](../../tuning/README.md) | [Task A Detailed Results](../../TaskA/results/readme.md) | [Task B Detailed Results](../../TaskB/results/readme.md) | [Task C Detailed Results](../../TaskC/results/readme.md) | [Task A Datasets](../../datasets/TaskA/README.md) | [Task B Datasets](../../datasets/TaskB/README.md) | [Task C Datasets](../../datasets/TaskC/README.md) | [Finetuning Datasets](../../datasets/Tuning/README.md) |**


## Finetuning Datasets


For task A for each class, we choose 8 samples per class from the train set. As well for task B and C, we have only considered those train that has been split with integration with task A. The obtained stat for GeoNames (tasks A, and B), WN18RR (task A), UMLS (NCI only for Task A, B, and C), and Schema.OrG (task B) is presented as followings:

| Dataset | Supported Task(s) | # of samples |
|:---:|:---:|:---:|
| WN18RR| A | 32 |
| GeoNames| A,B | 5102 |
| NCI| A, B, C | 911  |
| Schema.Org| B| 1068 |

Each dataset format has been changed to support our requirements for the training. Also, it is worth mentioning that we applied negative sampling for datasets but we ended-up up NOT using them during training process.
