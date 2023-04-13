
## Template Analysis 

|  Dataset   |                                                         Model                                                         |                                   $t_1$                                    |                                   $t_2$                                    |                                 $t_3$                                  |                                    $t_4$                                    |                                 $t_5$                                  |                                  $t_6$                                  |                                    $t_7$                                     |                                      $t_8$                                      |
|:----------:|:---------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------:|:--------------------------------------------------------------------------:|:----------------------------------------------------------------------:|:---------------------------------------------------------------------------:|:----------------------------------------------------------------------:|:-----------------------------------------------------------------------:|:----------------------------------------------------------------------------:|:-------------------------------------------------------------------------------:|
|  GeoNames  | BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>GPT2-Large<br>GPT2-XL<br>GPT3 <br> BLOOM-1b7 <br> BLOOM-3b |   42 <br> 38 <br> **53** <br> 49<br> 34 <br> 33 <br> 41 <br> 33 <br> 39    | **59** <br> 58 <br> 41 <br> 47 <br> 34 <br> 35 <br> **55** <br> 32 <br> 32 | 41 <br> 35 <br> 49 <br> 43 <br> 34 <br> 33 <br> 41 <br> 33 <br> **54** |  59<br> 55 <br> 43 <br> **56** <br> 33 <br> 35 <br> **55** <br> 33 <br> 32  | 39 <br> 36 <br> 48 <br> 44 <br> 33 <br> 33 <br> 45 <br> **34** <br> 45 | 47 <br> **62** <br> 42 <br> 48 <br> 34 <br> 34 <br> 52  <br> 35 <br> 34 |      44 <br> 32 <br> 45 <br> 46 <br> 34 <br> 33 <br> 39 <br> 33 <br> 47      | 58 <br> **62** <br> 36 <br> 48  <br> 34 <br> **39** <br> **55** <br> 33 <br> 32 |
|    UMLS    |         BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>GPT2-Large<br>GPT2-XL<br>GPT3<br>BLOOM-1b7 <br> BLOOM-3b        | **50** <br> 42 <br> 41 <br> **65** <br> 33 <br> 33<br> 48 <br>  33 <br> 33 |    43 <br> 50 <br> 44 <br> 48  <br> 35 <br> 37 <br> 49 <br> 32 <br> 37     |  45 <br> 44 <br> 49 <br> 49 <br> 32 <br> 33 <br> 52 <br> 33  <br> 32   | 45 <br> **56** <br> 35 <br> 43 <br> **38** <br> 35 <br> 46  <br> 33 <br> 36 |  48 <br> 45 <br> 50 <br> 59  <br> 33 <br> 33 <br> 52 <br> 34 <br> 33   |   43 <br> 52 <br> 42 <br> 44 <br> 33 <br> 36 <br> 46 <br> **35** <br> 36    | 47 <br> 43 <br> **52** <br> 50  <br> 33 <br> 33 <br> **53**  <br> 33 <br> 33 |  47 <br> 55 <br> 44 <br> 45   <br> 35 <br> **39** <br> 46<br> 33  <br> **38**   |
| Schema.ORG |         BERT-Large<br>BART-Large<br>Flan-T5-Large<br>Flan-T5-XL<br>GPT2-Large<br>GPT2-XL<br>GPT3<br>BLOOM-1b7 <br> BLOOM-3b        |            47 <br> 35 <br> 37 <br> 40   <br> 34 <br> 33<br> 50             |            44 <br> 47 <br> 38 <br> 34   <br> 34 <br> 33 <br> 49            |         46 <br> 42 <br> 39 <br> 34  <br> 33 <br> 33<br> **51**         |        46 <br> **54** <br> 39 <br> **42**   <br> 33 <br> 34 <br> 47         |         46  <br> 41 <br> 39 <br> 36   <br> 33 <br> 33 <br> 49          |          42 <br> 50 <br> 41 <br> 34   <br> 34 <br> 33 <br>  50          |             45 <br> 44 <br> 43 <br> 33   <br> 34 <br> 33 <br> 50             |           **48**  <br> 49 <br> **51** <br> 34 <br> 33 <br> 33<br> 49            |

* The obtained optimum templates utilized for experiments

## Optimum Results

|  Dataset   | $BERT_{large}$ | $BART_{large}$  | $Flan-T5_{large}$ | $Flan-T5_{xl}$ | $GPT2_{large}$ |  $GPT2_{xl}$   | $GPT3_{babbage}$ | $BLOOM_{1b7}$ | $BLOOM_{3b7}$ |
|:----------:|:--------------:|:---------------:|:-----------------:|:--------------:|:--------------:|:--------------:|:----------------:|:-------------:|:-------------:|
|  GeoNames  |   59 $(t_2)$   | 62 $(t_6, t_8)$ |    53 $(t_1)$     |   56 $(t_4)$   |       34       |   39 $(t_8)$   |        55        |  34 $(t_5)$   |  54 $(t_3)$   |
|    UMLS    |   50 $(t_1)$   |   56 $(t_4)$    |    52 $(t_7)$     |   65 $(t_1)$   |   38 $(t_1)$   | 39 $(t_8)$     |    53 $(t_7)$    |  35 $(t_6)$   |  38 $(t_8)$   |
| Schema.ORG |   48 $(t_8)$   |   54 $(t_4)$    |    51 $(t_8)$     |   42 $(t_4)$   |      34        |   34 $(t_8)$   |    51 $(t_3)$    |               |               |


## Model descriptions

- MLMs:
  * $BERT_{large}$: BERT-Large LM with prompt-based inference and without fine-tuning

- Encoder-Decoders:
  * $Flan-T5_{large}$: Flan-T5-Large LM with prompt-based inference and without fine-tuning
  * $Flan-T5_{xl}$: Flan-T5-XL LM with prompt-based inference and without fine-tuning
  * $BART_{large}$: BART-Large LM with prompt-based inference and without fine-tuning
