import pandas as pd

from models.scores import ScorePrediction


def fill_predictions(week):
    path = '../DATA/Results/game_scores'
    games = pd.read_csv(path)
    week_games = games[games.week == int(week)]
    guess = ScorePrediction()
    print('predicting games')
    week_games[['predicted_home_score', 'predicted_away_score', 'predicted_spread']] = \
        week_games.apply(guess.get_predictions, home_team=week_games.home_team,
                         away_team=week_games.away_team, axis=1)[['predicted_home_score', 'predicted_away_score',
                                                                  'predicted_spread']]
    week_games.to_csv('../DATA/Results/Predictions_Week_' + str(self.week))
    print('DONE')
