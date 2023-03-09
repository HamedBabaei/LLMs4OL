

## Template Analysis (with baseline model)

| Dataset  |                          Model                          |            $t_1$             |               $t_2$                |             $t_3$             |                    $t_4$                    |            $t_5$            |             $t_6$             |            $t_7$             |                $t_8$                |
|:--------:|:-------------------------------------------------------:|:----------------------------:|:----------------------------------:|:-----------------------------:|:-------------------------------------------:|:---------------------------:|:-----------------------------:|:----------------------------:|:-----------------------------------:|
|  WN18RR  | BERT-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BART-Large | 2.19<br>0.17<br>2.81<br>0.01 | 9.36<br>19.70<br>**40.26**<br>0.28 | 9.18<br>5.54<br>17.83<br>0.22 | 19.41<br>**31.26**<br>**52.21**<br>**2.16** | 4.72<br>0.0<br>0.01<br>0.01 | 19.34<br>3.03<br>7.75<br>0.03 | 9.93<br>5.70<br>18.47<br>0.0 | **27.85**<br>26.80<br>18.85<br>0.19 |
| Geoname  | BERT-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BART-Large |  **44.20**<br><br><br>11.86  |       33.62<br><br><br>0.69        |     34.33<br><br><br>2.59     |           40.48 <br><br><br>1.23            |   26.28<br><br><br>25.13    |    28.49<br><br><br>25.98     |    12.02<br><br><br>8.41     |     35.21<br><br><br>**26.88**      |
|   NCI    | BERT-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BART-Large |     9.94<br><br><br>7.09     |        9.76<br><br><br>7.87        |     2.61 <br><br><br>5.14     |            2.90<br><br><br>6.32             |  **11.09**<br><br><br>9.10  |  10.96 <br><br><br>**9.94**   |     1.12<br><br><br>7.24     |        1.36 <br><br><br>8.26        |
| SNOMEDCT | BERT-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BART-Large |    19.83<br><br><br>19.16    |     8.02<br><br><br>**19.81**      |     1.06<br><br><br>4.16      |            0.12<br><br><br>4.04             | **21.10**<br><br><br>17.54  |    12.76<br><br><br>17.89     |    0.45<br><br><br>10.06     |        0.04<br><br><br>9.43         |
|  MEDCIN  | BERT-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BART-Large |    7.33<br><br><br>11.67     |     1.25<br><br><br>**12.65**      |     0.14<br><br><br>2.27      |            0.05<br><br><br>2.31             |  **8.71**<br><br><br>9.40   |     1.19<br><br><br>9.22      |     0.08<br><br><br>5.47     |        0.01<br><br><br>4.82         |

* The obtained optimum templates utilized for experiments

## Optimum Results

| Dataset  | $BERT_{large}$ | $Flan-T5_{large}$ | $Flan-T5_{xl}$ | $BART_{large}$ |
|:--------:|:--------------:|:-----------------:|:--------------:|:--------------:|
|  WN18RR  | 27.85 $(t_8)$  |   31.26 $(t_4)$   | 52.21 $(t_4)$  |  2.16 $(t_4)$  |
| Geoname  | 44.20 $(t_1)$  |                   |                | 26.88 $(t_8)$  |
|   NCI    | 11.09 $(t_5)$  |                   |                |  9.94 $(t_6)$  |
| SNOMEDCT | 21.10 $(t_5)$  |                   |                | 19.81 $(t_2)$  | 
|  MEDCIN  |  8.71 $(t_5)$  |                   |                | 12.65 $(t_2)$  |


## Model descriptions

- MLMs:
  * $BERT_{large}$: BERT-Large LM with prompt-based inference and without fine-tuning

- Encoder-Decoders:
  * $Flan-T5_{large}$: Flan-T5-Large LM with prompt-based inference and without fine-tuning
  * $Flan-T5_{xl}$: Flan-T5-XL LM with prompt-based inference and without fine-tuning
  * $BART_{large}$: BART-Large LM with prompt-based inference and without fine-tuning
