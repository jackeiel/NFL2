#### NFL Score Predictions

Weekly pick found in ./DATA/Results

Week 2 Picks Available 

Run on command line

`pipenv install`

Run in shell:

`>>>from models.scores import ScorePrediction`

`>>>guess = ScorePrediction()`

`>>>guess.get_predictions(home_team, away_team)`

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