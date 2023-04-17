
## Results

|  Dataset   | $BERT_{large}$ | $BART_{large}$ | $Flan-T5_{large}$ | $Flan-T5_{xl}$ | $GPT2_{large}$ | $GPT2_{xl}$ | $GPT3$ | $BLOOM_{1b7}$ | $BLOOM_{3b}$ |$BLOOM_{7b1}$ |
|:----------:|:--------------:|:--------------:|:-----------------:|:--------------:|:--------------:|:-----------:|:------:|:-------------:|:------------:| :------------:| 
|  UMLS      |       32       |       41       |        48         |       48       |       43       |     43        |   40   |      43       |      43      | | 




## Model descriptions

- Encoder LMs:
  * $BERT$: BERT-Large LM with prompt-based inference and without fine-tuning

- Encoder-Decoder LMs:
  * $Flan-T5$: Flan-T5-Large and Flan-T5-XL LMs with prompt-based inference and without fine-tuning
  * $BART$: BART-Large LM with prompt-based inference and without fine-tuning

- Decoder LMs: 
  * $GPT-3$: GPT-3-babbage-001 LM with prompt-based inference and without fine-tuning
  * $BLOOM$: BLOOM-1b7 and BLOOM-3b LM with prompt-based inference and without fine-tuning