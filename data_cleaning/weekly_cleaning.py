import pandas as pd

from data_cleaning import big_clean

def weekly_clean(week):
    master = pd.read_csv('./DATA/master/NFL.csv')
    new = pd.read_csv('./DATA/play_by_play_data/regular_season/reg_pbp_week_'+str(week)+'.csv',
                      low_memory=False)

    new_cleaned = big_clean.big_clean(new)

    new_master = pd.concat(master, new_cleaned, sort=False)

    new_master.to_csv('./DATA/master/NFL.csv')