import shelve

import pandas as pd
from sklearn.linear_model import LinearRegression

#create a function that takes two parameters
#team, opponent: average each feature

'''
What I want to do is to get an offensive average, and a defensive average for all of these 
features. 
For instance get moving average of yards_per_play for 'team'... THEN also get the average
yards_per_play for the opponent for the last five games where there were the opponent.
Take the average of those two, then plug into the model. Get a score for your team. 

Do the same thing for the other team. 

Subtract home team score from away team score and we get our predicted spread. 
'''

#or should this be a new class, when instantiated, it sets a bunch of the necessary parameters based upon
# team depentend time series analysis?
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

class ScorePrediction:
    def __init__(self):
        # this loads the most current dataset
        data = pd.read_csv('./DATA/master/NFL.csv', index_col='game_date')
        data.index = pd.DatetimeIndex(data.index)
        self.features = ['drive',
                    'goal_to_go',
                    'air_yards',
                    'yards_after_catch',
                    'punt_blocked',
                    'first_down_rush',
                    'first_down_pass',
                    'first_down_penalty',
                    'interception',
                    'punt_inside_twenty',
                    'tackled_for_loss',
                    'qb_hit',
                    'pass_attempt',
                    'sack',
                    'punt_attempt',
                    'fumble',
                    'return_yards',
                    'third_down_perc',
                    'fourth_down_perc',
                    'pass_perc',
                    'yards_per_deep_pass',
                    'yards_per_rush',
                    'yards_per_short_pass',
                    'yards_per_play',
                    'home']

        # self.team = data.team
        # self.opponent = data.opponent
        self.data = data

    def get_predictions(self, home_team, away_team):


        target = ['team_score']
        # self.home_team = home_team
        # self.away_team = away_team

        off_data = self.data[(self.data.team == home_team) | (self.data.team == away_team)]
        def_data = self.data[(self.data.opponent == home_team) | (self.data.opponent == away_team)]

        # df for projected home stat output
        home_off_stats = off_data[off_data.team == home_team]
        home_off_stats = home_off_stats[self.features]
        home_off_stats = home_off_stats.sort_index().rolling(4).mean().tail(1)

        away_def_stats = def_data[def_data.opponent == away_team]
        away_def_stats = away_def_stats[self.features]
        away_def_stats = away_def_stats.sort_index().rolling(4).mean().tail(1)

        home_projections = home_off_stats.append(away_def_stats, sort=False)
        home_projections = pd.DataFrame(data=home_projections.mean()).transpose()

        # don't forget to set this...
        home_projections[['home']] = 1

        # df for project away stat output
        away_off_stats = off_data[off_data.team == away_team]
        away_off_stats = away_off_stats[self.features]
        away_off_stats = away_off_stats.sort_index().rolling(4).mean().tail(1)

        home_def_stats = def_data[def_data.opponent == home_team]
        home_def_stats = home_def_stats[self.features]
        home_def_stats = home_def_stats.sort_index().rolling(4).mean().tail(1)

        away_projections = away_off_stats.append(home_def_stats, sort=False)
        away_projections = pd.DataFrame(data=away_projections.mean()).transpose()
        away_projections[['home']] = 0

        self.home_projections = home_projections
        self.away_projections = away_projections

        with shelve.open('./models/models') as db:
            key = 'model1'
            fit = db[key]

            self.home_prediction = fit.predict(home_projections)[0]
            self.away_prediction = fit.predict(away_projections)[0]

        return pd.DataFrame(data={'home_team':home_team, 'away_team': away_team,
                                  'predicted_home_score':self.home_prediction,
                                  'predicted_away_score':self.away_prediction,
                                  'predicted_spread':self.away_prediction-self.home_prediction,
                                  'model':key}, index=range(0,1))
