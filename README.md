### NFL Score Predictions

**Current Record Against the Spread**  
**45 - 26**  

Plots found in fig/  
Weekly picks found in DATA/Predictions/  
Outcomes found in DATA/Results/  

For most up to date predictions: 

Run

`$ pipenv install`  
`$ pipenv shell`  
`$ python`  

`>>> from models.scores import ScorePrediction`  
`>>> guess = ScorePrediction()`  
`>>> guess.get_predictions(home_team='DAL', away_team='NYG')`



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