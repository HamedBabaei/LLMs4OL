
<h1 align="center">LLMs4OL: Large Language Models for <br> Ontology Learning 
</h1>

**| [LLMs4OL Paradigm](./README.md#llms4ol-paradigm) | [Task A: Term Typing](./TaskA/README.md) | [Task B: Type Taxonomy Discovery](./TaskB/README.md) | [Task C: Type Non-Taxonomic Relation Extraction](./TaskC/README.md) | [Few-Shot Learning](./FSL/README.md) | [Task A Detailed Results](./TaskA/results/readme.md) | [Task B Detailed Results](./TaskB/results/readme.md) | [Task C Detailed Results](./TaskC/results/readme.md) | [Task A Datasets](./datasets/TaskA/README.md) | [Task B Datasets](./datasets/TaskB/README.md) | [Task C Datasets](./datasets/TaskC/README.md) | [Few-Shot Learning Datasets](./datasets/FSL/README.md) |**

--------------

Ontology Learning (OL) addresses the challenge of knowledge acquisition and representation  in a variety of domains. Recent advances in NLP and the emergence of Large Language Models, which have shown a capability to be good at crystallizing knowledge and patterns from vast text sources, we introduced the **LLMs4OL: Large Language Models for Ontology Learning** paradigm as a empirical study of LLMs for automated construction of ontologies from various domains.  The LLMs4OL paradigm tests *Does the capability of LLMs to capture intricate linguistic relationships translate effectively to OL, given that OL mainly relies on automatically extracting and structuring knowledge from natural language text?*.

### Table of Contents
- [LLMs4OL Paradigm](#llms4ol-paradigm)
- [LLMs4OL Paradigm Setups](#llms4ol-paradigm-setups)
    - [Tasks](#tasks)
    - [Datasets](#datasets)
    - Results
    - Experimental LLMs
- How to run.
    - Software Dependencies and Requirements
- Citations


## LLMs4OL Paradigm
<div align="center"><img src="images/LLMs4OL.jpg" /></div>
<div align="center">Figure 1: The LLMs4OL task paradigm is an end-to-end conceptual framework for learning ontologies in different knowledge domain</div>

<br>
The LLMs4OL paradigm offers a conceptual framework to accelerate the automated construction of ontologies exclusively by domain experts. OL tasks are based on the ontology primitives which consist of:

1. Corpus preparation – selecting and collecting the source texts to build the ontology. 
2. Terminology extraction – identifying and extracting relevant terms from the source text.
3. Term typing – grouping similar terms as conceptual types. 
4. Taxonomy construction – identifying the “is-a” hierarchies between types.
5. Relationship extraction – identifying and extracting “non-is-a” or semantic relationships between types
6. Axiom discovery – discovering constraints and inference rules for the ontology

Toward realizing LLMs4OL, we empirically ground three core tasks of OL leveraging LLMs as a foundational basis for future work. They are presented as:

- **Term Typing**
- **Type Taxonomy Discovery** -- for type "is-a" taxonomy construction
- **Type Non-Taxonomic Relation Extraction** -- for type "non-is-a" taxonomy construction

## LLMs4OL Paradigm Setups

The LLMs4OL task paradigm is an end-to-end conceptual framework for learning ontologies in different knowledge domains with aim of automation of ontology learning. 

### Tasks

The tasks within the blue arrow (in Figure-1) are the three OL tasks empirically validated. For each task we created a directory with detailed description of the task informations as follows:

- [Task A. Term Typing](./TaskA/README.md) 
- [Task B. Type Taxonomy Discovery](./TaskB/README.md)
- [Task C. Type Non-Taxonomic Relation Extraction](./TaskC/README.md)

### Datasets
To comprehensively assess LLMs for the three OL tasks we cover a variety of ontological knowledge domain sources, i.e. lexicosemantics – WN18RR (WordNet), geography – GeoNames,
biomedicine – NCI, MEDICIN, SNOMEDCT, and web content types – Schema.Org. These sources are different for each task, so for each task the detailed information is avaliable as follows:

- [Task A. Term Typing Datasets](./datasets/TaskA/README.md): GeoNames, NCI, MEDICIN, SNOMEDCT, and WN18RR
- [Task B. Type Taxonomy Discovery Datasets](./datasets/TaskB/README.md): GeoNames, Schema.Org, and UMLS
- [Task C. Type Non-Taxonomic Relation Extraction Datasets](./datasets/TaskC/README.md): UMLS


### Results

### Experimental LLMs

## Repository Structure



## How to run

### Requirements
