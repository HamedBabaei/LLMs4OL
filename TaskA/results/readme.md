

## Template Analysis (with baseline model)

| Dataset | Level | Model | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|WN18RR |-|BERT-Large<br>Flap-T5-Large| 2.29<br>0 | 10.62<br> | 9.595<br> | 21.992 | 5.079<br>| 21.915<br> | 9.906<br> | **32.269**<br>|
|Geoname|Level-1|BERT-Large| 23.322 | 20.268 | 17.837 | **24.791** | 12.505 | 15.676 | 3.752 | 20.988 |
| NCI|Level-1|BERT-Large| - |- | -  | - | **0.109** | 0.063 | 0.009  | 0.000 |
|SNOMEDCT|Level-1|BERT-Large |-|-|-|- | 0.048 | **0.053** | 0.001 | 0.004 |
|MEDICIN|Level-1|BERT-Large |-|-|-|- |  0.000 | 0.000 |  0.000 | 0.000 |

* The obtained optimum templates utilized for experimentations

## Obtained Results

| Dataset | | $BL_{i}$  |
|:---:|:---:|:---:|
|WN18RR | |32.269 |
|Geoname|Level-1<br>Level-2<br>Level-3|  24.791<br>-<br>- |
| NCI |Level-1<br>Level-2<br>Level-3 | 0.109<br>-<br>- | 
|SNOMEDCT|Level-1<br>Level-2<br>Level-3| 0.053<br>-<br>- | 
|MEDICIN|Level-1<br>Level-2<br>Level-3| 0.0<br>-<br>-| 

## Model descriptions

* $BL_{i}$: BERT-Large LM with prompt-based inference and without finetunning

## Key findings

