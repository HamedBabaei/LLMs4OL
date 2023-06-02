<h1 align="center">LLMs4OL: Large Language Models for <br> Ontology Learning </h1>

**| [LLMs4OL Paradigm](./README.md#llms4ol-paradigm) | [Task A: Term Typing](./TaskA/README.md) | [Task B: Type Taxonomy Discovery](./TaskB/README.md) | [Task C: Type Non-Taxonomic Relation Extraction](./TaskC/README.md) | [Few-Shot Learning](./FSL/README.md) | [Task A Detailed Results](./TaskA/results/readme.md) | [Task B Detailed Results](./TaskB/results/readme.md) | [Task C Detailed Results](./TaskC/results/readme.md) | [Task A Datasets](./datasets/TaskA/README.md) | [Task B Datasets](./datasets/TaskB/README.md) | [Task C Datasets](./datasets/TaskC/README.md) | [Few-Shot Learning Datasets](./datasets/FSL/README.md) |**

<div align="center"><img src="images/LLMs4OL.jpg" /></div>
<div align="center">Figure 1: The LLMs4OL task paradigm is an end-to-end conceptual framework for learning ontologies in different knowledge domain </div>
<br>

Ontology Learning (OL) addresses the challenge of knowledge acquisition and representation in a variety of domains. Recent advances in NLP and the emergence of Large Language Models, which have shown a capability to be good at crystallizing knowledge and patterns from vast text sources, we introduced the **LLMs4OL: Large Language Models for Ontology Learning** paradigm as an empirical study of LLMs for automated construction of ontologies from various domains.  The LLMs4OL paradigm tests *Does the capability of LLMs to capture intricate linguistic relationships translate effectively to OL, given that OL mainly relies on automatically extracting and structuring knowledge from natural language text?*.

### Table of Contents
- [Repository Structure](#repository-structure)
- [LLMs4OL Paradigm](#llms4ol-paradigm)
- [LLMs4OL Paradigm Setups](#llms4ol-paradigm-setups)
    - [Tasks](#tasks)
    - [Datasets](#datasets)
    - [Results](#results)
    - [Experimental LLMs](#experimental-llms)
- [Experiments](#experiments)
- [How to run tasks](#how-to-run-tasks)
- [Requirements](#requirements)
- [Citation](#citation)


## Repository Structure
```
.
└── LLMs4OL                       <- root directory of the repository
    ├── FSL                       <- Few-Shot Learning directory
    │   └── ...
    ├── TaskA                     <- Term Typing task directory
    │   └── ...
    ├── TaskB                     <- Type Taxonomy Discovery task directory
    │   └── ...
    ├── TaskC                     <- Type Non-Taxonomic Relation Extraction task directory
    │   └── ...
    ├── assets                    <- artifacts directory 
    │   ├── LLMs                  <- contains pretrained LLMs
    │   ├── FSL                   <- contains fine-tuned LLMs (for training you should create this)
    │   ├── WordNetDefinitions    <- contains wordnet word definitions
    │   └── CountryCodes          <- GeoNames country codes
    ├── datasets                  <- contains datasets
    │   ├── FSL                   <- contains few-shot learning training datasets
    │   ├── TaskA                 <- contains directories for task A sources
    │   ├── TaskB                 <- contains directories for task B sources
    │   └── TaskC                 <- contains directories for task C sources
    ├── images                    <- contains the figures
    ├── README.md                 <- README file for documenting the service.
    └── requirements.txt          <- contains Python requirements listed
```


## LLMs4OL Paradigm

The LLMs4OL paradigm offers a conceptual framework to accelerate the automated construction of ontologies exclusively by domain experts. OL tasks are based on the ontology primitives which consist of:

1. Corpus preparation – selecting and collecting the source texts to build the ontology. 
2. Terminology extraction – identifying and extracting relevant terms from the source text.
3. Term typing – grouping similar terms as conceptual types. 
4. Taxonomy construction – identifying the “is-a” hierarchies between types.
5. Relationship extraction – identifying and extracting “non-is-a” or semantic relationships between types
6. Axiom discovery – discovering constraints and inference rules for the ontology

Toward realizing LLMs4OL, we empirically ground three core tasks of OL leveraging LLMs as a foundational basis for future work. They are presented as:

- **Term Typing**
- **Type Taxonomy Discovery**  
- **Type Non-Taxonomic Relation Extraction**

## LLMs4OL Paradigm Setups

The LLMs4OL task paradigm is an end-to-end conceptual framework for learning ontologies in different knowledge domains with the aim of automation of ontology learning. 

### Tasks

The tasks within the blue arrow (in Figure-1) are the three OL tasks empirically validated. For each task, we created a directory with a detailed description of the task information as follows:

- [Task A. Term Typing](./TaskA/README.md) 
- [Task B. Type Taxonomy Discovery](./TaskB/README.md)
- [Task C. Type Non-Taxonomic Relation Extraction](./TaskC/README.md)

### Datasets
To comprehensively assess LLMs for the three OL tasks we cover a variety of ontological knowledge domain sources, i.e. lexicosemantics – [WN18RR](https://github.com/TimDettmers/ConvE) (WordNet), geography – [GeoNames](http://www.geonames.org/),
biomedicine – [NCI](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NCI/index.html), [MEDICIN](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/MEDCIN/index.html), [SNOMEDCT](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/SNOMEDCT_US/index.html), and web content types – [Schema.Org](https://schema.org/). These sources are different for each task, so for each task, the detailed information is available as follows:

- [Task A. Term Typing Datasets](./datasets/TaskA/README.md): GeoNames, NCI, MEDICIN, SNOMEDCT, and WN18RR
- [Task B. Type Taxonomy Discovery Datasets](./datasets/TaskB/README.md): GeoNames, Schema.Org, and [UMLS](https://lhncbc.nlm.nih.gov/semanticnetwork/)
- [Task C. Type Non-Taxonomic Relation Extraction Datasets](./datasets/TaskC/README.md): [UMLS](https://lhncbc.nlm.nih.gov/semanticnetwork/)


### Results

The evaluation metric for Task A is reported as the mean average precision at k (MAP@K), where k = 1, And evaluations for Tasks B and C are reported in terms of the standard F1-score based on precision and recall. Complete and detailed results for tasks are presented in the following tables:

- [Task A. Term Typing Detailed Results Table](./TaskA/results/readme.md) 
- [Task B. Type Taxonomy Discovery Detailed Results Table](./TaskB/results/readme.md) 
- [Task C. Type Non-Taxonomic Relation Extraction Detailed Results Table](./TaskC/results/readme.md)

### Experimental LLMs

We created experimentations using five different LMs. These LMs described as followings:

- Encoder-Only:
    - **[BERT-Large](https://huggingface.co/bert-large-uncased)** with 340M parameters
- Encoder-Decoder:
    - **[BART-Large](https://huggingface.co/facebook/bart-large)** with 400M parameters 
    - **[Flan-T5-Large](https://huggingface.co/google/flan-t5-large)** with 780M parameters
    - **[Flan-T5-XL](https://huggingface.co/google/flan-t5-xl)** with 3B parameters
- Decoder-Only:
    - **[BLOOM-1b7](https://huggingface.co/bigscience/bloom-1b7)** with 1.7B parameters
    - **[BLOOM-3b](https://huggingface.co/bigscience/bloomz-3b)** with 3B parameters
    - **[GPT-3](https://platform.openai.com/docs/models/gpt-3)** with 175B parameters

## Experiments
First we created prompt templates based on existing experimental language models and their nature -- specifically for tasks A and B we created 8 templates per source, and for task C only a single template --. Next, we probe LMs as zero-shot testing. More later we attempt to boost the performance of two LLMs (Flan-T5-Large and Flan-T5-XL) in the form of few-shot learning using predefined prompt templates (different than zero-shot testing) and we test the model using zero-shot testing prompt templates. 

Prompt templates for zero-shot testing are represented as follows:
|Dataset| Task | prompt templates path | answer set mapper path|
|:---:|:---:|:---:|:---:|
|WN18RR | A | [`datasets/TaskA/WN18RR/templates.json`](datasets/TaskA/WN18RR/templates.json)| `datasets/TaskA/WN18RR/label_mapper.json` |
|GeoNames | A | `datasets/TaskA/Geonames/templates.json`| `datasets/TaskA/Geonames/label_mapper.json`|
|NCI, MEDICIN, SNOMEDCT | A | `datasets/TaskA/UMLS/templates.json`| `datasets/TaskA/UMLS/label_mapper.json`|
|Schema.Org, UMLS, GeoNames |‌ B | `datasets/TaskB/templates.txt`| `datasets/TaskB/label_mapper.json`|
|UMLS | C | `datasets/TaskC/templates.txt`| `datasets/TaskC/label_mapper.json`|

### Zero-Shot Learning
All the initial experimentations with LLMs have been conducted in a zero-shot setting to probe knowledge from LLMs. 

### Few-Shot Learning

## How to run tasks

## Requirements

## Citation
>‌ ...
