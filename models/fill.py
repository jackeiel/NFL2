import pandas as pd

from models.scores import ScorePrediction
from data_cleaning import gather


def fill_predictions(week):
    path = './DATA/Predictions/game_scores.csv'
    games = pd.read_csv(path)
    week_games = games[games.week == int(week)]
    guess = ScorePrediction()
    print('predicting games')

    printout = pd.concat([guess.get_predictions(home, away) for (home, away) in
                          zip(week_games.home_team, week_games.away_team)])

    printout.index = range(0,len(week_games))
    print(printout)

    week_games.loc[:,'predicted_home_score'] = printout['predicted_home_score'].values
    week_games.loc[:,'predicted_away_score'] = printout.loc[:, 'predicted_away_score'].values
    week_games.loc[:,'predicted_spread'] = printout.loc[:, 'predicted_spread'].values

    week_games = week_games.loc[:,['game_id', 'week', 'home_team', 'predicted_home_score', 'away_team',
                                   'predicted_away_score', 'predicted_spread']]

    # retrieve Ceasar spread/odds
    vegas_lines = gather.get_lines()

    new = week_games.merge(vegas_lines, how='left', on=['home_team', 'away_team',
                                                   'week'])

    #TODO implement 'bet' algo

    new.to_csv('./DATA/Predictions/Predictions_Week_' + str(week)+'.csv')

    print('DONE')

def fill_bets(df_predictions):
    # take a df... will have to read in the latest predictions
    # use algo on desk at home...
    pass