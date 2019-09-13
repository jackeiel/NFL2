import pandas as pd

from data_cleaning import big_clean

def weekly_clean(week):
    master = pd.read_csv('./DATA/master/NFL.csv', index_col=0)
    new = pd.read_csv('./DATA/play_by_play_data/regular_season/2019/reg_pbp_week_'+str(week)+'.csv',
                      low_memory=False, index_col=0)

    print('cleaning')
    new_cleaned = big_clean.big_clean(new)
    new_cleaned.reset_index(inplace=True)
    print('combining')
    new_master = master.append(new_cleaned, sort=True)
    print('writing')
    new_master.to_csv('./DATA/master/NFL.csv')