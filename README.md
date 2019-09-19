### NFL Score Predictions

Weekly pick found in ./DATA/Results
<<<<<<< HEAD

Week 3 Picks Available 


#### Record
**Overall** 

Week 3 Picks Available


**Overvall for 2019 Season**
20 - 11
*Week 2*
9 - 6 (excluded NYJ game w/ Darnold out)
*Week 1*
11 - 5

The app relies on an external R script to gather play by play data every week. 
A comprehensive script is being written to handle weekly updates smoothly.

For the time being
`$ Rscript ./DATA/R/scrape.R`
will gather data from the week specified (must go into script and edit week variable)



Run on command line

`pipenv install`
`pipenv shell`



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