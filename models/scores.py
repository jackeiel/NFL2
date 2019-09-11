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

features = ['drive',
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

target = ['team_score']

class ScorePrediction:
    def __init__(self):
        # set self.yards, self.completion_perc, etc, then use these for the predict function
        data= pd.read_csv('./DATA/master/NFL.csv', parse_dates=True, index_col='game_date')
        data.index = pd.DatetimeIndex(data.index)

        self.data = data

    def get_predictions(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team

        self.off_data = self.data[(self.data.team == self.home_team) | (self.data.team == self.away_team)]
        self.def_data = self.data[(self.data.opponent == self.home_team) | (self.data.opponent == self.away_team)]

        # df for projected home stat output
        home_off_stats = self.off_data[self.off_data.team == self.home_team]
        home_off_stats = home_off_stats.sort_index().rolling(4).mean().tail(1)

        away_def_stats =  self.def_data[self.def_data.opponent == self.away_team]
        away_def_stats = away_def_stats.sort_index().rolling(4).mean().tail(1)

        home_projections = pd.concat([home_off_stats, away_def_stats], sort=False)
        self.home_projections = pd.DataFrame(data=home_projections.mean()).transpose()

        #don't forget to set this...
        self.home_projections[['home']] = 1

        # df for project away stat output
        away_off_stats = self.off_data[self.off_data.team == self.away_team]
        away_off_stats = away_off_stats.sort_index().rolling(5).mean().tail(1)

        home_def_stats = self.def_data[self.def_data.opponent == self.home_team]
        home_def_stats = home_def_stats.sort_index().rolling(5).mean().tail(1)

        away_projections = pd.concat([away_off_stats, home_def_stats], sort=False)
        self.away_projections = pd.DataFrame(data=away_projections.mean()).transpose()
        self.away_projections[['home']] = 0

        db = shelve.open('./models/model1')
        key = 'model2'
        fit = db[key]

        self.home_prediction = fit.predict(self.home_projections[features])[0]
        self.away_prediction = fit.predict(self.away_projections[features])[0]

        return pd.DataFrame(data={'team':[self.home_team, self.away_team],
                                  'predicted_score':[self.home_prediction, self.away_prediction],
                                  'predicted_spread':[self.away_prediction-self.home_prediction,
                                            self.home_prediction-self.away_prediction],
                                  'model':key})
