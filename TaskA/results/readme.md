

## Template Analysis (with baseline model)

| Dataset  |                          Model                          |            $t_1$             |               $t_2$                |             $t_3$             |                    $t_4$                    |            $t_5$            |             $t_6$             |            $t_7$             |                $t_8$                |
|:--------:|:-------------------------------------------------------:|:----------------------------:|:----------------------------------:|:-----------------------------:|:-------------------------------------------:|:---------------------------:|:-----------------------------:|:----------------------------:|:-----------------------------------:|
|  WN18RR  | BERT-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BART-Large | 2.19<br>0.17<br>2.81<br>0.01 | 9.36<br>19.70<br>**40.26**<br>0.28 | 9.18<br>5.54<br>17.83<br>0.22 | 19.41<br>**31.26**<br>**52.21**<br>**2.16** | 4.72<br>0.0<br>0.01<br>0.01 | 19.34<br>3.03<br>7.75<br>0.03 | 9.93<br>5.70<br>18.47<br>0.0 | **27.85**<br>26.80<br>18.85<br>0.19 |
| Geoname  |                       BERT-Large                        |                              |                                    |                               |                                             |                             |                               |                              |                                     |
|   NCI    |                       BERT-Large                        |                              |                                    |                               |                                             |                             |                               |                              |                                     |
| SNOMEDCT |                       BERT-Large                        |                              |                                    |                               |                                             |                             |                               |                              |                                     |
| MEDICIN  |                       BERT-Large                        |                              |                                    |                               |                                             |                             |                               |                              |                                     |

* The obtained optimum templates utilized for experiments

## Optimum Results

| Dataset  | $BERT_{large}$ | $Flan-T5_{large}$ | $Flan-T5_{xl}$ | $BART_{large}$ |
|:--------:|:--------------:|:-----------------:|:--------------:|:--------------:|
|  WN18RR  | 27.85 $(t_8)$  |   31.26 $(t_4)$   | 52.21 $(t_4)$  |  2.16 $(t_4)$  |
| Geoname  |                |                   |                |                |
|  NCI     |                |                   |                |                |
| SNOMEDCT |                |                   |                |                | 
| MEDICIN  |                |                   |                |                |


## Model descriptions

- MLMs:
  * $BERT_{large}$: BERT-Large LM with prompt-based inference and without fine-tuning

- Encoder-Decoders:
  * $Flan-T5_{large}$: Flan-T5-Large LM with prompt-based inference and without fine-tuning
  * $Flan-T5_{xl}$: Flan-T5-XL LM with prompt-based inference and without fine-tuning
  * $BART_{large}$: BART-Large LM with prompt-based inference and without fine-tuning
