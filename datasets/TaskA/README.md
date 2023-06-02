
**| [LLMs4OL Paradigm](../../README.md#llms4ol-paradigm) | [Task A: Term Typing](../../TaskA/README.md) | [Task B: Type Taxonomy Discovery](../../TaskB/README.md) | [Task C: Type Non-Taxonomic Relation Extraction](../../TaskC/README.md) | [Few-Shot Learning](../../FSL/README.md) | [Task A Detailed Results](../../TaskA/results/readme.md) | [Task B Detailed Results](../../TaskB/results/readme.md) | [Task C Detailed Results](../../TaskC/results/readme.md) | [Task A Datasets](../../datasets/TaskA/README.md) | [Task B Datasets](../../datasets/TaskB/README.md) | [Task C Datasets](../../datasets/TaskC/README.md) | [Few-Shot Learning Datasets](../../datasets/FSL/README.md) |**


## Task A. Term Typing Datasets
Datasets for task A are:
1. GeoNames: https://www.geonames.org: size is 8M
2. NCI: (UMLS version 2022AB from Metathesaurus)
3. SNOMEDCT_US: (UMLS version 2022AB from Metathesaurus)
4. MEDCIN: (UMLS version 2022AB from Metathesaurus)
5. [WN18RR](https://github.com/TimDettmers/ConvE)

Stats in Processed-3
- Szie of dataset is:8_781_375
- Level 1 class FQs:
```
P    3190806
S    1778015
H    1640789
T    1267499
A     434874
L     368481
V      47458
R      40408
U      13045
```

### NCI
- `#` of samples in NCI entity detection dataset is: 120_222

### SNOMEDCT_US
SNOMEDCT_US sub dataset stats:
- `#` of samples in SNOMEDCT_US entity detection dataset is: 347_968


### MEDCIN


MEDCIN sub dataset stats:
- `#` of samples in MEDCIN entity detection dataset is: 346_286

UMLS source are:‌ 

- https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html
- Downloaded release version of 2022AB from Metathesaurus Full Subset: https://download.nlm.nih.gov/umls/kss/2022AB/umls-2022AB-metathesaurus-full.zip

### WN18RR
WN18RR source are:
- https://github.com/TimDettmers/ConvE
- https://everest.hds.utc.fr/doku.php?id=en:transe


- The size of relation detection train set is: 86835
- The size of relation detection test set is: 3134
- The size of relation detection valid set is: 3034
- The size of entity type detection train set is: 40559
- The size of entity type detection test set is: 5323
- The size of entity type detection valid set is: 5173
