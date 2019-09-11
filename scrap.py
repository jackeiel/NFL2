# from data_cleaning import clean

# cleans all regular season and post season game data from 2009 onward
# for year in range(2009, 2019):
#     clean.agg_plays('./DATA/play_by_play_data/regular_season/reg_pbp_'+str(year)+'.csv',
#                     './DATA/games_data/regular_season/reg_games_'+str(year)+'.csv')
#     clean.agg_plays('./DATA/play_by_play_data/post_season/post_pbp_' + str(year) + '.csv',
#                     './DATA/games_data/post_season/post_games_' + str(year) + '.csv')

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

from models.scores import ScorePrediction
guess = ScorePrediction()
print(guess.get_predictions('NE', 'PIT'))
