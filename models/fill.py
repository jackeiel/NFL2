import pandas as pd

from models.scores import ScorePrediction


def fill_predictions(week):
    path = './DATA/Results/game_scores.csv'
    games = pd.read_csv(path)
    week_games = games[games.week == int(week)]
    guess = ScorePrediction()
    print('predicting games')

    printout = pd.concat([guess.get_predictions(home, away) for (home, away) in
                          zip(week_games.home_team, week_games.away_team)])
    printout.index = range(0,16)
    print(printout)

    week_games.loc[:,'predicted_home_score'] = printout['predicted_home_score'].values
    week_games.loc[:,'predicted_away_score'] = printout['predicted_away_score'].values
    week_games.loc[:,'predicted_spread'] = printout['predicted_spread'].values

    week_games.to_csv('./DATA/Results/Predictions_Week_' + str(week)+'.csv')

    print('DONE')
