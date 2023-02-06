

## Template Analysis (with baseline model)

| Dataset | Level | Model | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|WN18RR |-|BERT-Large| 2.29 | 10.62 | 9.595 | 21.992 | 5.079 | 21.915 | 9.906 | **32.269**|
|Geoname|Level-1|BERT-Large| 23.322 | 20.268 | 17.837 | **24.791** | 12.505 | 15.676 | 3.752 | 20.988 |
| NCI|Level-1|BERT-Large<br>BioBERT-Large<br>BioClinicalBERT| <br> <br>  |<br>  <br> | <br>  <br> <br>  | <br> <br>  | **0.109**<br>0.000<br>0.000 | 0.063<br>0.000<br>0.000 | 0.009<br>0.000<br>0.000 | 0.000<br>0.000<br>0.000|
|SNOMEDCT|Level-1|BERT-Large<br>BioBERT-Large<br>BioClinicalBERT|<br> <br> |<br> |<br> |<br> | 0.048<br>0.000 <br>0.000 | **0.053**<br>0.000<br> 0.000  | 0.001<br>0.000 <br>0.000 | 0.004<br>0.000 <br>0.000 |
|MEDICIN|Level-1|BERT-Large<br>BioBERT-Large<br>BioClinicalBERT| <br><br> |<br> <br> |<br> <br> | <br> <br>| 0.000<br>0.000<br>0.000  | 0.000<br>0.000<br>0.000  | 0.000<br>0.000<br>0.000  | 0.000<br>0.000<br>0.000 |

## Results

| Dataset | | BL  |
|:---:|:---:|:---:|
|WN18RR | |32.269 |
|Geoname|Level-1<br>Level-2<br>Level-3|  24.791<br>-<br>- |
| NCI |Level-1<br>Level-2<br>Level-3 | 0.109<br>-<br>- | 
|SNOMEDCT|Level-1<br>Level-2<br>Level-3| 0.053<br>-<br>- | 
|MEDICIN|Level-1<br>Level-2<br>Level-3| 0.0<br>-<br>-| 



* BL: BERT-Large