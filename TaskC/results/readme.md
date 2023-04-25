
## Results

|  Dataset   | $BERT_{large}$ | $BART_{large}$ | $Flan-T5_{large}$ | $Flan-T5_{xl}$ | $GPT3$ | $BLOOM_{1b7}$ | $BLOOM_{3b}$ | $Flan-T5_{large}-ours$ | $Flan-T5-XL-ours$ |
|:----------:|:--------------:|:--------------:|:-----------------:|:--------------:|:------:|:-------------:|:------------:|:----------------------:|:-----------------:|
|  UMLS      |     40.10      |     42.35      |       46.02       |   **49.52**    | 38.84  |     43.12     |    42.70     |         49.05          |       53.05       |



## Model descriptions

- Encoder LMs:
  * $BERT$: BERT-Large LM with prompt-based inference and without fine-tuning

- Encoder-Decoder LMs:
  * $Flan-T5$: Flan-T5-Large and Flan-T5-XL LMs with prompt-based inference and without fine-tuning
  * $BART$: BART-Large LM with prompt-based inference and without fine-tuning

- Decoder LMs: 
  * $GPT-3$: GPT-3-babbage-001 LM with prompt-based inference and without fine-tuning
  * $BLOOM$: BLOOM-1b7 and BLOOM-3b LM with prompt-based inference and without fine-tuning