

## Template Analysis (with baseline model)

| Dataset  |                              Model                               |                        $t_1$                        |                     $t_2$                     |                     $t_3$                     |                         $t_4$                         |                    $t_5$                    |                   $t_6$                    |                  $t_7$                   |                     $t_8$                      |
|:--------:|:----------------------------------------------------------------:|:---------------------------------------------------:|:---------------------------------------------:|:---------------------------------------------:|:-----------------------------------------------------:|:-------------------------------------------:|:------------------------------------------:|:----------------------------------------:|:----------------------------------------------:|
|  WN18RR  | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>GPT-3 |        2.19<br>0.01<br>0.17<br>2.81<br>15.32        |  9.36<br>0.28<br>19.70<br>**40.26**<br>26.55  |  9.18<br>0.22<br>5.54<br>17.83<br>**37.86**   | 19.41<br>**2.16**<br>**31.26**<br>**52.21**<br>27.57  |     4.72<br>0.01<br>0.0<br>0.01<br>8.47     |  19.34<br>0.03 <br>3.03<br>7.75<br>27.13   |  9.93<br>0.0<br>5.70<br>18.47<br>27.51   |  **27.85**<br>0.19<br>26.80<br>18.85<br>24.65  |
| Geoname  |     BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>GPT3      | **44.19**<br>11.86<br>14.46<br>**38.72** <br> 22.42 |    33.63<br>0.69<br>8.56<br>24.80<br> 8.72    |     34.35<br>2.57<br>15.81<br>22.92<br>-      |       40.48<br>1.22<br>9.76<br>29.60 <br> 7.50        |    26.28<br>25.12<br>11.39<br>19.44<br>-    |   28.56<br>25.98<br>14.69<br>21.13<br> -   |   12.00<br>8.42<br>9.65<br>23.47<br>-    | 35.28<br>**26.86**<br>**17.15**<br>25.07<br> - |
|   NCI    |     BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>GPT3      |       9.94<br>7.09<br>4.59<br>4.44 <br> 9.30        |    9.76<br>7.87<br>5.06<br>5.65 <br> 9.19     |    2.61<br>5.14<br>7.53<br>7.41<br> 11.03     |  2.90<br>6.32 <br>**8.96**<br>**9.83**<br>**12.74**   |  **11.09**<br>9.10<br>3.06<br>2.12<br>9.37  | 10.96 <br>**9.94**<br>4.25<br>3.29<br>8.75 |   1.12<br>7.24<br>5.48<br>3.87<br>9.14   |     1.36 <br>8.26<br>5.84<br>6.28 <br>9.11     |
| SNOMEDCT |     BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>GPT3      |     19.83<br>19.16<br>19.26<br>25.21 <br> 21.06     | 8.02<br>**19.81**<br>19.89<br>26.23 <br>20.33 |   1.06<br>4.16 <br>21.04<br>30.09<br> 22.73   | 0.12<br>4.04<br>**24.32**<br>**31.65** <br> **24.36** | **21.10**<br>17.54<br>8.07<br>7.21<br>19.20 |  12.76<br>17.89<br>8.90<br>8.22<br>18.99   | 0.45<br>10.06<br>11.54<br>15.58<br>20.20 |    0.04<br>9.43<br>12.92<br>17.22<br>20.09     |
|  MEDCIN  |     BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>GPT3      |      7.33<br>11.67<br>9.30<br>15.24 <br> 22.40      |  1.25<br>**12.65**<br>8.08<br>15.89<br>22.50  | 0.14<br>2.27<br>10.97<br>18.04 <br> **25.72** |   0.05<br>2.31<br>**12.96**<br>**18.51** <br>24.91    |  **8.71**<br>9.40<br>2.89<br>4.47<br>19.75  |   1.19<br>9.22<br>3.59<br>5.44<br>17.80    |  0.08<br>5.47<br>6.71<br>11.14<br>19.92  |     0.01<br>4.82<br>6.78<br>11.09<br>18.57     |

* The obtained optimum templates utilized for experiments

## Optimum Results

| Dataset  | $BERT_{large}$ | $BART_{large}$ | $Flan-T5_{large}$ | $Flan-T5_{xl}$ |    $GPT-3$    |
|:--------:|:--------------:|:--------------:|:-----------------:|:--------------:|:-------------:|
|  WN18RR  | 27.85 $(t_8)$  |  2.16 $(t_4)$  |   31.26 $(t_4)$   | 52.21 $(t_4)$  | 37.86 $(t_3)$ |
| Geoname  | 44.19  $(t_1)$ | 26.86 $(t_8)$  |   17.15 $(t_8)$   | 38.72 $(t_4)$  |               |
|   NCI    | 11.09 $(t_5)$  |  9.94 $(t_6)$  |   8.96  $(t_4)$   |  9.83 $(t_4)$  | 12.74 $(t_4)$ |
| SNOMEDCT | 21.10 $(t_5)$  | 19.81 $(t_2)$  |   24.32 $(t_4)$   | 31.65 $(t_4)$  | 24.36 $(t_4)$ |
|  MEDCIN  |  8.71 $(t_5)$  | 12.65 $(t_2)$  |   12.96 $(t_4)$   | 18.51 $(t_4)$  | 27.72 $(t_3)$ |


## Model descriptions

- MLMs:
  * $BERT_{large}$: BERT-Large LM with prompt-based inference and without fine-tuning

- Encoder-Decoders:
  * $Flan-T5_{large}$: Flan-T5-Large LM with prompt-based inference and without fine-tuning
  * $Flan-T5_{xl}$: Flan-T5-XL LM with prompt-based inference and without fine-tuning
  * $BART_{large}$: BART-Large LM with prompt-based inference and without fine-tuning
