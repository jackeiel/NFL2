import pandas as pd

# what I'd like to do is simply build a df with:
# home_team
# away_team
# predicted scores
# predicted over under
# vegas line
# vegas over under
# actual scores
# actual over under
# bet on who?
# win bet?

# basically this is a scraper and compiler
# need to find a good site to pull lines / over under from...

def bets(week):
    new = pd.read_csv(f'./DATA/Results/Predictions_Week_{week}.csv')
    actual_scores = pd.read_csv('./DATA/master/NFL.csv')

    # pull latest scores based on teams in predictions
    def pull_home_score(row):
        new =
        return row['home_score']