
## Template Analysis 

|  Dataset   |                                          Model                                           |                                  $t_1$                                   |                                   $t_2$                                    |                                 $t_3$                                  |                                    $t_4$                                     |                                 $t_5$                                  |                                  $t_6$                                  |                                   $t_7$                                   |                                  $t_8$                                  |
|:----------:|:----------------------------------------------------------------------------------------:|:------------------------------------------------------------------------:|:--------------------------------------------------------------------------:|:----------------------------------------------------------------------:|:----------------------------------------------------------------------------:|:----------------------------------------------------------------------:|:-----------------------------------------------------------------------:|:-------------------------------------------------------------------------:|:-----------------------------------------------------------------------:|
|  GeoNames  | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BLOOM-1b7<br>BLOOM-3b<br>GPT3 | 41.54 <br>  45.86<br>  59.74<br>  49.63<br>  49.63<br>  50.73<br>  46.32 |56.25<br>  50.45<br>  48.8<br>  45.58<br>  37.31<br>  46.04<br>  52.38 |42.64<br>  44.02<br>  54.13<br>  48.52<br>  49.63<br>  56.43<br>  44.48 |53.3<br>  52.75<br>  48.25<br>  54.13<br>  48.89<br>  40.62<br>  55.42 |44.39<br>  41.91<br>  45.03<br>  44.02<br>  49.9<br>  50.27<br>  48.06 |52.11<br>  51.37<br>  51.74<br>  48.16<br>  47.79<br>  49.54<br>  54.04 |  45.03<br>  36.94<br>  47.33<br>  50.55<br>  50.64<br>  56.15<br>  46.32  | 55.05<br>  57.81<br>  43.38<br>  44.3<br>  49.08<br>  45.12<br>  53.67  | 
|    UMLS    | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BLOOM-1b7<br>BLOOM-3b<br>GPT3 | 51.59 <br>  48.4<br>  50.12<br>  64.61<br>  50.85<br>  49.63<br>  53.31  |48.89<br>  54.79<br>  51.35<br>  50.36<br>  51.59<br>  52.08<br>  49.87 |49.63<br>  50.36<br>  55.77<br>  52.33<br>  50.85<br>  49.63<br>  51.1 |47.66<br>  52.57<br>  41.76<br>  43.98<br>  52.57<br>  51.59<br>  44.22 |51.84<br>  47.17<br>  49.63<br>  62.16<br>  50.85<br>  49.63<br>  52.57 |50.85<br>  54.05<br>  51.1<br>  45.94<br>  51.84<br>  51.84<br>  47.66 |  50.61<br>  45.94<br>  50.36<br>  52.82<br>  49.87<br>  49.38<br>  46.19  | 50.36<br>  53.07<br>  51.84<br>  41.27<br>  50.61<br>  52.57<br>  47.66 |
| Schema.ORG | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BLOOM-1b7<br>BLOOM-3b<br>GPT3 | 48.8 <br>  48.36<br>  48.54<br>  52.22<br>  49.95<br>  50.32<br>  50.42  |49.78<br>  49.08<br>  56.15<br>  49.81<br>  53.06<br>  48.01<br>  49.29 |49.71<br>  49.22<br>  50.7<br>  50.02<br>  49.95<br>  51.4<br>  51.24 |48.92<br>  53.06<br>  57.67<br>  51.63<br>  50.91<br>  50.11<br>  48.43 |50.51<br>  47.63<br>  40.73<br>  48.87<br>  49.67<br>  49.78<br>  48.52 |49.39<br>  50.25<br>  59.05<br>  50.11<br>  53.04<br>  51.24<br>  49.6 | 49.83<br>  47.05<br>  43.42<br>  49.83<br>  50.44<br>  52.27<br>  49.01   | 49.6<br>  52.03<br>  51.89<br>  50.88<br>  50.98<br>  49.01<br>  49.76  |

* The obtained optimum templates utilized for experiments

## Optimum Results

|  Dataset   | $BERT_{large}$ | $BART_{large}$  | $Flan-T5_{large}$ | $Flan-T5_{xl}$ |  $BLOOM_{1b7}$ | $BLOOM_{3b7}$ | $GPT3$|
|:----------:|:--------------:|:---------------:|:-----------------:|:--------------:|:--------------:|:----------------:|:-------------:|
|  GeoNames  |   56.25  | 57.81  | **59.74**  | 54.13  | 50.64  | 56.43  | 55.42 |
|    UMLS    |   51.84  | 54.79  | 55.77   | **64.61**|   52.57  |  52.57  | 52.57 |
| Schema.ORG |   50.51  | 53.06 | **59.05**   | 52.22 |   53.06  |  52.27  | 51.24 |

## Model descriptions

- Encoder LMs:
  * $BERT$: BERT-Large LM with prompt-based inference and without fine-tuning

- Encoder-Decoder LMs:
  * $Flan-T5$: Flan-T5-Large and Flan-T5-XL LMs with prompt-based inference and without fine-tuning
  * $BART$: BART-Large LM with prompt-based inference and without fine-tuning

- Decoder LMs: 
  * $GPT-3$: GPT-3-babbage-001 LM with prompt-based inference and without fine-tuning
  * $BLOOM$: BLOOM-1b7 and BLOOM-3b LM with prompt-based inference and without fine-tuning