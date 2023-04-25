
## Template Analysis 

|  Dataset   |                                                                  Model                                                                   |                                  $t_1$                                   |                                   $t_2$                                    |                                 $t_3$                                  |                                    $t_4$                                     |                                 $t_5$                                  |                                  $t_6$                                  |                                   $t_7$                                   |                                  $t_8$                                  |
|:----------:|:----------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------:|:--------------------------------------------------------------------------:|:----------------------------------------------------------------------:|:----------------------------------------------------------------------------:|:----------------------------------------------------------------------:|:-----------------------------------------------------------------------:|:-------------------------------------------------------------------------:|:-----------------------------------------------------------------------:|
|  GeoNames  |  BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BLOOM-1b7<br>BLOOM-3b<br>GPT3 <br>`Flan-T5-Large-ours`<br>`Flan-T5-XL-ours`  |  41.0<br>  38.11<br>  59.63<br>  49.37<br>  33.16<br>  35.85<br>  43.43 |51.69<br>  41.03<br>  48.24<br>  44.05<br>  31.04<br>  39.12<br>  51.74 |40.55<br>  40.55<br>  54.08<br>  45.09<br>  33.16<br>  53.92<br>  42.7 |48.7<br>  52.5<br>  48.24<br>  52.41<br>  32.83<br>  30.22<br>  53.2 |37.16<br>  39.09<br>  44.4<br>  43.92<br>  33.77<br>  35.62<br>  46.04 |41.07<br>  45.8<br>  51.3<br>  46.34<br>  33.53<br>  33.6<br>  52.56 |41.7<br>  36.67<br>  36.4<br>  49.98<br>  36.67<br>  48.26<br>  45.49 |54.54<br>  55.4<br>  38.44<br>  44.29<br>  32.92<br>  37.73<br>  52.62 |
|    UMLS    |  BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BLOOM-1b7<br>BLOOM-3b<br>GPT3 <br>`Flan-T5-Large-ours`<br>`Flan-T5-XL-ours`  | 48.21<br>  36.02<br>  47.55<br>  64.25<br>  33.71<br>  33.16<br>  51.58<br>  37.17<br>  63.69 |38.84<br>  48.21<br>  51.22<br>  46.53<br>  36.18<br>  37.23<br>  49.41<br>  48.66<br>  50.04 |41.46<br>  41.42<br>  55.32<br>  51.0<br>  33.71<br>  34.82<br>  49.86<br>  36.07<br>  36.91 |40.41<br>  49.9<br>  40.94<br>  41.54<br>  38.26<br>  35.77<br>  42.9<br>  42.12<br>  41.34 |45.88<br>  39.37<br>  49.45<br>  60.07<br>  33.71<br>  33.16<br>  50.57<br>  48.39<br>  78.12 |40.91<br>  47.47<br>  50.87<br>  42.83<br>  35.89<br>  35.89<br>  46.07<br>  46.65<br>  50.12 |41.04<br>  42.39<br>  44.23<br>  51.25<br>  33.27<br>  33.05<br>  45.36<br>  53.42<br>  79.25 |42.92<br>  45.46<br>  42.9<br>  41.18<br>  33.6<br>  37.48<br>  46.72<br>  35.97<br>  39.27 |
| Schema.ORG | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>BLOOM-1b7<br>BLOOM-3b<br>GPT3  <br>`Flan-T5-Large-ours`<br>`Flan-T5-XL-ours`  | 43.85<br>  34.62<br>  46.98<br>  42.7<br>  33.39<br>  41.64<br>  49.64 |41.17<br>  38.69<br>  49.92<br>  33.45<br>  47.83<br>  47.16<br>  49.28 |44.06<br>  39.28<br>  46.11<br>  33.59<br>  33.39<br>  47.98<br>  50.97 |43.2<br>  52.9<br>  54.78<br>  42.76<br>  39.77<br>  45.25<br>  48.03 |43.7<br>  38.2<br>  40.27<br>  36.69<br>  38.92<br>  39.73<br>  47.19 |40.05<br>  41.17<br>  54.47<br>  34.04<br>  48.56<br>  40.75<br>  48.63 |42.15<br>  43.26<br>  42.06<br>  33.75<br>  44.35<br>  51.28<br>  48.87 |43.72<br>  42.74<br>  47.93<br>  36.45<br>  39.57<br>  48.73<br>  49.48 |

* The obtained optimum templates utilized for experiments

## Optimum Results

|  Dataset   | $BERT_{large}$ | $BART_{large}$ | $Flan-T5_{large}$ | $Flan-T5_{xl}$ | $BLOOM_{1b7}$ | $BLOOM_{3b7}$ | $GPT3$ | $Flan-T5-Large-ours$ | $Flan-T5-XL-ours$ |
|:----------:|:--------------:|:--------------:|:-----------------:|:--------------:|:-------------:|:-------------:|:------:|:--------------------:|:-----------------:|
|  GeoNames  |    54.54       |     55.4       |     **59.63**     |     52.41      |   36.67       |     48.26     | 53.2   |                      |                   |
|    UMLS    |     48.21      |      49.9      |     55.32         |   **64.25**    |     38.26     |     37.48     | 51.58  |        53.42         |       79.25       |
| Schema.ORG |     44.06      |      52.9      |     **54.78**     |     42.70      |     48.56     |   51.28       | 50.97  |                      |                   |



## Model descriptions

- Encoder LMs:
  * $BERT$: BERT-Large LM with prompt-based inference and without fine-tuning

- Encoder-Decoder LMs:
  * $Flan-T5$: Flan-T5-Large and Flan-T5-XL LMs with prompt-based inference and without fine-tuning
  * $BART$: BART-Large LM with prompt-based inference and without fine-tuning

- Decoder LMs: 
  * $GPT-3$: GPT-3-babbage-001 LM with prompt-based inference and without fine-tuning
  * $BLOOM$: BLOOM-1b7 and BLOOM-3b LM with prompt-based inference and without fine-tuning