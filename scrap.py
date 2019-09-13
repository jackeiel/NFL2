from glob import glob
import pandas as pd

# from data_cleaning.big_clean import big_clean
# # combine all seasons into one massive master game file
# files = glob('./DATA/play_by_play_data/post_season/*.csv')
# files.extend(glob('./DATA/play_by_play_data/regular_season/*.csv'))
# print('files collected')
# master = pd.concat([pd.read_csv(file, low_memory=False) for file in files], sort=False)
# print('files combined')
# data = big_clean(master)
#
# data.to_csv('./DATA/master/NFL.csv')
# print('Done with Cleaning')

# from models import fill
# fill.fill_predictions(1)

# from data_cleaning import weekly_cleaning
# weekly_cleaning.weekly_clean(1)

from models import fill
fill.fill_predictions(2)