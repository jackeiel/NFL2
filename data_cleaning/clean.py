import pandas as pd
import numpy as np

def agg_plays(plays_path, games_path):

    '''
    Use agg_plays to clean csv files from ryurko's R NFL data scrapper and return game
    level data. csv files need to be from the same season (i.e. pre, reg, post season) or
    else game_id will not be matched properly

    :param plays_path: path name for a csv of play-by-play data and aggregates it into meaningful summary statistics
    :param games_path: path name for a csv of game data

    :return: cleaned dataframe where each line is a team's performance in that particular game
    '''

    all_plays = pd.read_csv(plays_path, parse_dates=['game_date'], low_memory=False)
    # variables related to offensive output
    VARS = ['game_id',
            'posteam', 'game_date',
            'ydsnet', 'yards_gained', 'air_yards',
            'yards_after_catch',
            'first_down_rush', 'first_down_pass', 'third_down_converted',
            'third_down_failed',
            'interception', 'fourth_down_converted',
            'complete_pass', 'rush_attempt','pass_attempt', 'rush_touchdown',
            'pass_touchdown']

    offensive_plays = all_plays[VARS]
    each_game = offensive_plays.groupby(['game_id', 'posteam','game_date'])
    sums = each_game.agg(np.sum)

    final = sums
    final['completion_perc'] = final.complete_pass / final.pass_attempt
    final['third_down_perc'] = final.third_down_converted / sum(final.third_down_failed,
                                                                final.third_down_converted)
    team = final.index.droplevel(['game_id', 'game_date'])
    final['team'] = team
    date = final.index.droplevel(['game_id','posteam'])
    final['game_date'] = date

    game_data = pd.read_csv(games_path)

    df = final.merge(game_data, how='left', on='game_id')

    #game_date = all_plays.groupby(['game_id', 'posteam'])['game_date']
    #df['game_date'] = game_date

    # returns new whether a team won or lost a particular game
    def win(row):
        if row['team'] == row['home_team']:
            if row['home_score'] > row['away_score']:
                return 1
            else:
                return 0
        if row['team'] == row['away_team']:
            if row['away_score'] > row['home_score']:
                return 1
            else:
                return 0
        else:
            # if tie, return 0
            return 0

    df['win'] = df.apply(win, axis=1)

    # returns the final score for a particular team
    def team_score(row):
        if row['team'] == row['home_team']:
            return row['home_score']
        else:
            return row['away_score']

    df['team_score'] = df.apply(team_score, axis=1)

    season = min(list(game_data.season.unique()))

    if 'regular' in plays_path:
        df.to_csv('./DATA/agg_data/regular_game_agg_'+str(season)+'.csv')
    if 'post' in plays_path:
        df.to_csv('./DATA/agg_data/post_game_agg_' + str(season)+'.csv')
    return print(str(season) + ' Complete')
