setwd("~/Python/NFL2/DATA/R")

library(nflscrapR)
ids = scrape_game_ids(2019)
week = 17

week_games = ids[ids$week==week,]
pbp = data.frame()
for (game in week_games$game_id){
pbp = rbind(pbp, scrape_game_play_by_play(game, 'reg', 2019))
}
name = paste('../play_by_play_data/regular_season/2019/reg_pbp_week_', week, sep='')
name = paste(name,'.csv', sep='')
write.csv(pbp, name)
print('done gathering play-by-play data')

