
## Results

|  Dataset   | $BERT_{large}$ | $BART_{large}$ | $Flan-T5_{large}$ | $Flan-T5_{xl}$ | $GPT2_{large}$ | $GPT2_{xl}$ |
|:----------:|:--------------:|:--------------:|:-----------------:|:--------------:|:--------------:|:-----------:|
|  UMLS      |       32       |       41       |        48         |       48       |       43       |     43        |


## Model descriptions

- MLMs:
  * $BERT_{large}$: BERT-Large LM with prompt-based inference and without fine-tuning

- Encoder-Decoders:
  * $Flan-T5_{large}$: Flan-T5-Large LM with prompt-based inference and without fine-tuning
  * $Flan-T5_{xl}$: Flan-T5-XL LM with prompt-based inference and without fine-tuning
  * $BART_{large}$: BART-Large LM with prompt-based inference and without fine-tuning
