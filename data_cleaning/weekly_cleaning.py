import pandas as pd

from data_cleaning import big_clean

def weekly_clean(week):
    master = pd.read_csv('./DATA/master/NFL.csv', index_col=0)
    master.index = pd.DatetimeIndex(master.index)

    new = pd.read_csv('./DATA/play_by_play_data/regular_season/2019/reg_pbp_week_'+str(week)+'.csv',
                      low_memory=False, index_col=0)

    print('cleaning')
    new_cleaned = big_clean.big_clean(new)
    new_cleaned.index = pd.DatetimeIndex(new_cleaned.index)

    print('combining')
    new_master = master.append(new_cleaned, sort=False)
    print('writing')
    new_master.to_csv('./DATA/master/NFL.csv')


def evaluate(week):
    def to_date(game_id):
        el = str(game_id)
        return '-'.join([el[:4], el[4:6], el[6:8]])

    weeks_predictions = pd.read_csv(f'DATA/Predictions/Predictions_Week_{week}.csv')
    weeks_predictions['game_date'] = pd.to_datetime(weeks_predictions.game_id.apply(to_date))

    full = pd.read_csv('DATA/master/NFL.csv', parse_dates=['game_date'])

    # gives us one row per game (instead of one row for each team)
    sub = full.loc[full.home_team == full.team,['game_date', 'home_team', 'away_team', 'total_home_score',
                                            'total_away_score', 'team', 'team_score', 'opponent']]

    joined = weeks_predictions.merge(sub, on=['game_date','home_team','away_team'])

    # TODO apply a win or not function, write to results folder
    def win_lose(df):
        if df.bets == df.home_team:
            if df.total_home_score + df.vegas_line_home > df.total_away_score:
                return 1
            else:
                return 0
        if df.bets == df.away_team:
            if df.total_home_score + df.vegas_line_home < df.total_away_score:
                return 1
            else:
                return 0

    joined['win_bet'] = joined.apply(win_lose, axis=1)

    final = joined[['game_id','game_date', 'week', 'home_team',
       'predicted_home_score', 'away_team', 'predicted_away_score',
       'predicted_spread', 'vegas_line_home', 'bets',
       'total_home_score', 'total_away_score', 'win_bet']]

    final.to_csv(f'DATA/Results/Week_{week}.csv')





