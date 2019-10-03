### NFL Score Predictions

Weekly pick found in ./DATA/Results

#### Record  
Week 3 Picks Available  
  
**Overvall for 2019 Season (through Week 2)**  
20 - 11  
*Week 2*  
9 - 6 (excluded NYJ game w/ Darnold out)  
*Week 1*  
11 - 5  

For current predictions: 

Run

`$ pipenv install`  
`$ pipenv shell`  
`$ python`  

`>>> from models.scores import ScorePrediction`  
`>>> guess = ScorePrediction()`  
`>>> guess.get_predictions(home_team='DAL', away_team='GB')`



home_team and away_team are team city abbreviations, listed in scores.py and here:

all_teams = ['HOU',
             'IND',
             'DAL',
             'SEA',
             'BAL',
             'LAC',
             'CHI',
             'PHI',
             'KC',
             'LA',
             'NE',
             'NO',
             'APR',
             'NPR',
             'ARI',
             'CAR',
             'PIT',
             'CIN',
             'DET',
             'GB',
             'DEN',
             'CRT',
             'IRV',
             'MIN',
             'WAS',
             'RIC',
             'TEN',
             'ATL',
             'BUF',
             'JAX',
             'AFC',
             'NFC',
             'OAK',
             'MIA',
             'NYG',
             'CLE',
             'SF',
             'TB',
             'NYJ',
             'JAC',
             'SD',
             'STL']