

## Template Analysis (with baseline model)

| Dataset  |                          Model                          |   T1   |   T2   |   T3   |     T4     |    T5     |    T6     |  T7   |     T8     |
|:--------:|:-------------------------------------------------------:|:------:|:------:|:------:|:----------:|:---------:|:---------:|:-----:|:----------:|
|  WN18RR  | BERT-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BART-Large |  2.19  |  9.36  |  9.18  |   19.41    |   4.72    |   19.34   | 9.93  | **27.85**  |
| Geoname  |                       BERT-Large                        | 23.322 | 20.268 | 17.837 | **24.791** |  12.505   |  15.676   | 3.752 |   20.988   |
|   NCI    |           BERT-Large                                    |   -    |   -    |   -    |     -      | **0.109** |   0.063   | 0.009 |   0.000    |
| SNOMEDCT |                       BERT-Large                        |   -    |   -    |   -    |     -      |   0.048   | **0.053** | 0.001 |   0.004    |
| MEDICIN  |                       BERT-Large                        |   -    |   -    |   -    |     -      |   0.000   |   0.000   | 0.000 |   0.000    |

* The obtained optimum templates utilized for experimentations

## Obtained Results

| Dataset  | $BERT_{large}$ | $Flan-T5_{large}$ | $Flan-T5_{xl}$ | $BART_{large}$ |
|:--------:|:--------------:|:-----------------:|:--------------:|:--------------:|
|  WN18RR  |   27.85(T8)    |                   |                |                |
| Geoname  |                |                   |                |                |
|  NCI     |                |                   |                |                |
| SNOMEDCT |                |                   |                |                | 
| MEDICIN  |                |                   |                |                |


## Model descriptions

* $BL_{nf}$: BERT-Large LM with prompt-based inference and without finetunning

## Key findings

