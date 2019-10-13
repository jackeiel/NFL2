from glob import glob
import pandas as pd

from data_cleaning.weekly_cleaning import weekly_clean
from models import fill

def data_init():
    from data_cleaning.big_clean import big_clean
    # combine all seasons into one massive master game file
    files = glob('./DATA/play_by_play_data/post_season/*.csv')
    files.extend(glob('./DATA/play_by_play_data/regular_season/*.csv'))
    print('files collected')
    master = pd.concat([pd.read_csv(file, low_memory=False) for file in files], sort=False)
    print('files combined')
    data = big_clean(master)

    data.to_csv('./DATA/master/NFL.csv')
    print('Done with Cleaning')

def auto(week):
    # week is the week I want to PREDICT
    weekly_clean(int(week)-1)
    fill.fill_predictions(int(week))
    print('done')

weeks = [1, 2, 3, 4, 5, 6]

def write_bets():
    for week in weeks:
        df = pd.read_csv(f'DATA/Predictions/Predictions_Week_{week}.csv')
        df['bets'] = df.apply(fill.fill_bets, axis=1)
        df.to_csv(f'DATA/Predictions/Predictions_Week_{week}.csv')

'''
install sklear 0.21.3
rebuild model in proper env (do everything in the env from now on ya idiot)
make week 1 predictions
run weekly cleaning for week 1
make week 2 predictions
run weekly cleaning for week 2
make week 3 predictions
'''