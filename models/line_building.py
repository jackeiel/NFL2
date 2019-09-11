import shelve

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv('./DATA/master/NFL.csv', index_col=0)
df.index = pd.to_datetime(df.index)

df['game_date'] = df.index
boo = df.game_date>pd.to_datetime('06/01/2014')
df = df[boo]

df['third_down_perc'] = df.third_down_converted / sum(df.third_down_converted, df.third_down_failed)
df['fourth_down_perc'] = df.fourth_down_converted / sum(df.fourth_down_converted, df.fourth_down_failed)
df['pass_perc'] = df.complete_pass / sum(df.complete_pass, df.incomplete_pass)
df['spread'] = df.total_home_score - df.total_away_score
df['yards_per_deep_pass'] = df.deep_pass_yards / df.deep_pass_attempt
df['yards_per_rush'] = df.rush_yards / df.rush_attempt
df['yards_per_short_pass'] = df.short_pass_yards / df.short_pass_attempt
df['yards_per_play'] = df.yards_gained / df.total_plays


def home(row):
    if row['team'] == row['home_team']:
        return 1
    else:
        return 0


df['home'] = df[['team', 'home_team']].apply(home, axis=1)

score_vars = ['sp', 'total_home_score', 'total_away_score', 'touchdown', 'pass_touchdown', 'rush_touchdown',
             'extra_point_attempt', 'two_point_attempt', 'field_goal_attempt', 'field_goal_result',
             'extra_point_result', 'two_point_conv_result', 'safety', 'return_touchdown',
              'defensive_two_point_attempt', 'defensive_two_point_conv', 'defensive_extra_point_attempt',
              'defensive_extra_point_conv', 'win', 'spread']

df = df.drop(score_vars, axis=1)
noise = ['shotgun', 'qb_dropback', 'third_down_converted', 'third_down_failed',
         'fourth_down_converted', 'fourth_down_failed', 'punt_in_endzone',
         'punt_out_of_bounds', 'punt_downed', 'kickoff_inside_twenty',
         'kickoff_in_endzone', 'kickoff_out_of_bounds', 'kickoff_downed',
         'fumble_forced', 'fumble_not_forced', 'fumble_out_of_bounds',
         'solo_tackle', 'own_kickoff_recovery', 'own_kickoff_recovery_td',
         'kickoff_attempt', 'assist_tackle', 'lateral_reception',
         'lateral_rush', 'lateral_return', 'lateral_recovery',
         'fumble_recovery_1_yards', 'fumble_recovery_2_yards','total_plays',
         'complete_pass', 'incomplete_pass', 'deep_pass_yards',
         'deep_pass_attempt', 'rush_yards', 'rush_attempt', 'yards_gained',
         'short_pass_yards', 'short_pass_attempt', 'qb_kneel',
        'qb_spike', 'qb_scramble', 'punt_fair_catch', 'fumble_lost',
        'deep_pass_complete', 'short_pass_complete', 'kickoff_fair_catch',
        'no_huddle', 'penalty', 'pass_length', 'penalty_yards']
df = df.drop(noise, axis=1)

identifiers = ['home_team', 'away_team', 'team', 'opponent', 'team_score', 'game_date'] #also included spread as its our target

data = df.drop(identifiers, axis=1)
data = data.fillna(0)

xtrain, xtest, ytrain, ytest = train_test_split(data, df.team_score,
                                               test_size=0.30)
lm = LinearRegression()
lm.fit(xtrain, ytrain)

s = shelve.open('./models/model1')
s['model2'] = lm
s.close()
