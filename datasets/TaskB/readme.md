
## Geonames:
- Source of information for feature codes: https://www.geonames.org/export/
  - `featureCodes.txt` : name and description for feature classes and feature codes
  - feature classes: 
  ```
    A: country, state, region,...
    H: stream, lake, ...
    L: parks,area, ...
    P: city, village,...
    R: road, railroad 
    S: spot, building, farm
    T: mountain,hill,rock,... 
    U: undersea
    V: forest,heath,...
  ```


## UMLS:
- Link to semantic network of the UMLS: https://lhncbc.nlm.nih.gov/semanticnetwork/ with the following files:
```
SRDEF|Basic information about the Semantic Types and Relations|RT,UI,STY/RL,STN/RTN,DEF,EX,UN,NH,ABR,RIN|10|187|44474|
SRFLD|Field Description|COL,DES,REF,FIL|4|21|683|
SRSTRE1|Fully inherited set of Relations (UIs)|UI,UI,UI|3|6704|107264|
SRSTRE2|Fully inherited set of Relations (Names)|STY,RL,STY|3|6704|341866|
SRSTR|Structure of the Network|STY/RL,RL,STY/RL,LS|4|603|30436|
```

## Hierarchy stats

| Dataset name |                  Path                  | Size |
|:-------------:|:--------------------------------------:|:----:|
|   Geonames    | `Geonames/processed/feature_codes.csv` | 680  |
|      NCI      |  `NCI/processed/semantic_network.csv`  | 104  |
|  SNOMEDCT_US  |      `SNOMEDCT_US/processed/semantic_network.csv`| 104  |
|    MEDCIN     |  `MEDCIN/processed/semantic_network.csv`|  76  |

note: for MEDCIN we added the following semantic networks to create hierarchy in efficient way. However they don't exist in MEDCIN:
```json
{
  "A": "Entity",
  "A1.2": "Anatomical Structure",
  "A1.1": "Organism",
  "A1": "Physical Object",
  "A2": "Conceptual Entity",
  "B": "Event",
  "B2.2": "Natural Phenomenon or Process",
  "A2.9": "Group"
}
```