import pandas as pd
import numpy as np


def big_clean(df):
    '''
    :param path: dataframe of play_by_play data scrapped by ryurko with nflscrapR
    :return: cleaned, aggregated dataframe where each row is a team's performance in a game
    '''
    data = df # pd.read_csv(path, low_memory=False)

    non_id = [col for col in data.columns if 'player' not in col]
    data = data[non_id]

    # data['game_date'] = pd.to_datetime(data.game_date)
    to_drop = ['play_id', 'desc', 'yrdln', 'play_type', 'pass_location', 'run_location', 'run_gap', 'timeout_team',
               'solo_tackle_1_team', 'solo_tackle_2_team', 'assist_tackle_1_team', 'assist_tackle_2_team',
               'fumbled_1_team', 'fumbled_2_team', 'fumble_recovery_2_team', 'return_team', 'penalty_team',
               'replay_or_challenge_result', 'penalty_type', 'side_of_field', 'timeout', 'posteam_timeouts_remaining',
               'defteam_timeouts_remaining']

    def passes(x):
        if x == 'short':
            return 1
        if x == 'deep':
            return 2
        else:
            return np.nan

    data.loc[:,'pass_length'] = data.pass_length.apply(passes)

    def field_goal(x):
        if x == 'good':
            return 3
        if x == 'missed':
            return 0
        if x == 'blocked':
            return 0
        else:
            return np.nan

    data.loc[:,'field_goal_result'] = data.field_goal_result.apply(field_goal)

    def extra_point(x):
        if x == 'good':
            return 1
        if x == 'failed':
            return 0
        if x == 'blocked':
            return 0
        else:
            return np.nan

    data.loc[:,'extra_point_result'] = data.extra_point_result.apply(extra_point)

    def two_point(x):
        if x == 'success':
            return 2
        if x == 'failure':
            return 0
        else:
            return np.nan

    data.loc[:,'two_point_conv_result'] = data.two_point_conv_result.apply(two_point)
    data = data.drop(to_drop, axis=1)

    def deep_pass_attempt(x):
        if x == 2:
            return 1
        else:
            return 0

    def short_pass_attempt(x):
        if x == 1:
            return 1
        else:
            return 0

    data.loc[:,'deep_pass_attempt'] = data.pass_length.apply(deep_pass_attempt)
    data.loc[:,'short_pass_attempt'] = data.pass_length.apply(short_pass_attempt)

    def deep_pass_complete(df):
        if df['pass_length'] == 2:
            if df['complete_pass'] == 1:
                return 1
            if df['complete_pass'] == 0:
                return 0
            else:
                return np.nan

    def short_pass_complete(df):
        if df['pass_length'] == 1:
            if df['complete_pass'] == 1:
                return 1
            if df['complete_pass'] == 0:
                return 0
            else:
                return np.nan

    data.loc[:,'deep_pass_complete'] = data[['pass_length', 'complete_pass']].apply(deep_pass_complete, axis=1)
    data.loc[:,'short_pass_complete'] = data[['pass_length', 'complete_pass']].apply(short_pass_complete, axis=1)

    # deep pass yards
    def deep_pass_yards(df):
        if df['deep_pass_complete'] == 1:
            return df['yards_gained']
        else:
            return np.nan

    # short pass yards
    def short_pass_yards(df):
        if df['short_pass_complete'] == 1:
            return df['yards_gained']
        else:
            return np.nan

    # all rush yards
    def rush_yards(df):
        if df['rush_attempt'] == 1:
            return df['yards_gained']
        else:
            return np.nan

    data.loc[:,'deep_pass_yards'] = data[['deep_pass_complete', 'yards_gained']].apply(deep_pass_yards, axis=1)
    data.loc[:,'short_pass_yards'] = data[['short_pass_complete', 'yards_gained']].apply(short_pass_yards, axis=1)
    data.loc[:,'rush_yards'] = data[['rush_attempt', 'yards_gained']].apply(rush_yards, axis=1)

    more_drop_vars = [col for col in data.columns if 'epa' in col or 'wp' in col]
    data = data.drop(more_drop_vars, axis=1)

    num_vars = [col for col in data.columns if data[col].dtype != 'object']

    num_data = data[num_vars]
    num_data.loc[:, 'posteam'] = data['posteam']
    num_data.loc[:, 'game_date'] = data['game_date']

    agg_num_data = num_data.groupby(['game_id', 'posteam', 'game_date']).agg(np.sum)

    agg_num_data.loc[:,'drive'] = num_data.groupby(['game_id', 'posteam', 'game_date'])['drive'].agg(np.max)
    agg_num_data.loc[:,'total_home_score'] = num_data.groupby(['game_id', 'posteam',
                                                         'game_date'])['total_home_score'].agg(np.max)
    agg_num_data.loc[:,'total_away_score'] = num_data.groupby(['game_id', 'posteam',
                                                         'game_date'])['total_away_score'].agg(np.max)
    agg_num_data.loc[:,'team'] = agg_num_data.index.droplevel(['game_id', 'game_date'])
    agg_num_data.loc[:,'total_plays'] = agg_num_data.pass_attempt + agg_num_data.rush_attempt
    agg_num_data.loc[:,'home_team'] = data.groupby(['game_id', 'posteam', 'game_date'])['home_team'].first()
    agg_num_data.loc[:,'away_team'] = data.groupby(['game_id', 'posteam', 'game_date'])['away_team'].first()

    def win(row):
        if row['team'] == row['home_team']:
            if row['total_home_score'] > row['total_away_score']:
                return 1
            else:
                return 0
        if row['team'] == row['away_team']:
            if row['total_away_score'] > row['total_home_score']:
                return 1
            else:
                return 0
        else:
            # if tie, return 0
            return 0

    agg_num_data.loc[:,'win'] = agg_num_data.apply(win, axis=1)

    def opp(row):
        if row['team'] == row['home_team']:
            return row['away_team']
        else:
            return row['home_team']

    def team_score(row):
        if row['team'] == row['home_team']:
            return row['total_home_score']
        else:
            return row['total_away_score']

    def home(row):
        if row['team'] == row['home_team']:
            return 1
        else:
            return 0

    agg_num_data.loc[:,'team_score'] = agg_num_data.apply(team_score, axis=1)

    agg_num_data.loc[:,'opponent'] = agg_num_data.apply(opp, axis=1)

    agg_num_data.index = agg_num_data.index.droplevel(['game_id', 'posteam'])

    useless_sums = ['yardline_100', 'quarter_seconds_remaining', 'half_seconds_remaining', 'game_seconds_remaining',
                    'quarter_end', 'qtr', 'down', 'ydstogo', 'ydsnet', 'kick_distance', 'home_timeouts_remaining',
                    'away_timeouts_remaining', 'posteam_score', 'defteam_score', 'score_differential',
                    'posteam_score_post', 'defteam_score_post', 'score_differential_post', 'replay_or_challenge', 'ep']
    useless_sums.extend([col for col in agg_num_data.columns if 'prob' in col])
    df = agg_num_data.drop(useless_sums, axis=1)

    df.loc[:,'third_down_perc'] = df.third_down_converted / (df.third_down_converted + df.third_down_failed)
    df.loc[:,'fourth_down_perc'] = df.fourth_down_converted / (df.fourth_down_converted + df.fourth_down_failed)
    df.loc[:,'pass_perc'] = df.complete_pass / (df.complete_pass + df.incomplete_pass)
    df.loc[:,'spread'] = df.total_home_score - df.total_away_score
    df.loc[:,'yards_per_deep_pass'] = df.deep_pass_yards / df.deep_pass_attempt
    df.loc[:,'yards_per_rush'] = df.rush_yards / df.rush_attempt
    df.loc[:,'yards_per_short_pass'] = df.short_pass_yards / df.short_pass_attempt
    df.loc[:,'yards_per_play'] = df.yards_gained / df.total_plays

    df.loc[:,'home'] = df.apply(home, axis=1)

    df = df.drop(['touchback'], axis=1)

    return df.fillna(0)