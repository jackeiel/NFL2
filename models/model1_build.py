import shelve

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def model1():
    df = pd.read_csv('./DATA/master/NFL.csv', index_col=0)
    df.index = pd.to_datetime(df.index)

    df['game_date'] = df.index
    boo = df.game_date>pd.to_datetime('06/01/2014')
    df = df[boo]

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

    identifiers = ['home_team', 'away_team', 'team', 'opponent', 'team_score', 'game_date']
    data = df.drop(identifiers, axis=1)
    data = data.fillna(0)

    xtrain, xtest, ytrain, ytest = train_test_split(data[features], df.team_score,
                                                   test_size=0.30)
    lm = LinearRegression()
    lm.fit(xtrain, ytrain)
    with shelve.open('./models/model1') as db:
        db['model1'] = lm
