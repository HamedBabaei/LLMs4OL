

## Template Analysis (with baseline model)

| Dataset  |                          Model                          |              $t_1$               |                $t_2$                |              $t_3$              |                    $t_4$                    |               $t_5$                |               $t_6$                |              $t_7$              |                $t_8$                |
|:--------:|:-------------------------------------------------------:|:--------------------------------:|:-----------------------------------:|:-------------------------------:|:-------------------------------------------:|:----------------------------------:|:----------------------------------:|:-------------------------------:|:-----------------------------------:|
|  WN18RR  | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL |   2.19<br>0.01<br>0.17<br>2.81   | 9.36<br>0.28<br>19.70<br>**40.26**  |  9.18<br>0.22<br>5.54<br>17.83  | 19.41<br>**2.16**<br>**31.26**<br>**52.21** |    4.72<br>0.01<br>0.0<br>0.01     |   19.34<br>0.03 <br>3.03<br>7.75   |  9.93<br>0.0<br>5.70<br>18.47   | **27.85**<br>0.19<br>26.80<br>18.85 |
| Geoname  | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL |    **44.20**<br>11.86<br><br>    |        33.62<br>0.69<br><br>        |      34.33<br>2.59<br><br>      |          40.48<br>1.23   <br><br>           |       26.28<br>25.13<br><br>       |       28.49<br>25.98<br><br>       |      12.02<br>8.41<br><br>      |     35.21<br>**26.88**<br><br>      |
|   NCI    | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL |   9.94<br>7.09<br>4.59<br>4.44   |    9.76<br>7.87<br>5.06<br>5.65     |  2.61<br>5.14<br>7.53<br>7.41   |    2.90<br>6.32 <br>**8.96**<br>**9.83**    | **11.09**<br>9.10<br>3.06<br>2.12  | 10.96 <br>**9.94**<br>4.25<br>3.29 |  1.12<br>7.24<br>5.48<br>3.87   |    1.36 <br>8.26<br>5.84<br>6.28    |
| SNOMEDCT | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL | 19.83<br>19.16<br>19.26<br>25.21 | 8.02<br>**19.81**<br>19.89<br>26.23 | 1.06<br>4.16 <br>21.04<br>30.09 |   0.12<br>4.04<br>**24.32**<br>**31.65**    | **21.10**<br>17.54<br>8.07<br>7.21 |   12.76<br>17.89<br>8.90<br>8.22   | 0.45<br>10.06<br>11.54<br>15.58 |   0.04<br>9.43<br>12.92<br>17.22    |
|  MEDCIN  | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL |  7.33<br>11.67<br>9.30<br>15.24  | 1.25<br>**12.65**<br>8.08<br>15.89  |    0.14<br>2.27<br>10.97<br>    |        0.05<br>2.31<br>**12.96**<br>        |    **8.71**<br>9.40<br>2.89<br>    |      1.19<br>9.22<br>3.59<br>      |    0.08<br>5.47<br>6.71<br>     |      0.01<br>4.82<br>6.78<br>       |

* The obtained optimum templates utilized for experiments

## Optimum Results

| Dataset  | $BERT_{large}$  | $BART_{large}$ | $Flan-T5_{large}$ | $Flan-T5_{xl}$ |
|:--------:|:---------------:|:--------------:|:-----------------:|:--------------:|
|  WN18RR  | 27.85 $(t_8)$   |  2.16 $(t_4)$  |   31.26 $(t_4)$   | 52.21 $(t_4)$  |
| Geoname  |  44.20 $(t_1)$  | 26.88 $(t_8)$  |                   |                |
|   NCI    |  11.09 $(t_5)$  |  9.94 $(t_6)$  |   8.96  $(t_4)$   |  9.83 $(t_4)$  |
| SNOMEDCT |  21.10 $(t_5)$  | 19.81 $(t_2)$  |   24.32 $(t_4)$   | 31.65 $(t_4)$  | 
|  MEDCIN  |  8.71 $(t_5)$   | 12.65 $(t_2)$  |   12.96 $(t_4)$   |                |


## Model descriptions

- MLMs:
  * $BERT_{large}$: BERT-Large LM with prompt-based inference and without fine-tuning

- Encoder-Decoders:
  * $Flan-T5_{large}$: Flan-T5-Large LM with prompt-based inference and without fine-tuning
  * $Flan-T5_{xl}$: Flan-T5-XL LM with prompt-based inference and without fine-tuning
  * $BART_{large}$: BART-Large LM with prompt-based inference and without fine-tuning
