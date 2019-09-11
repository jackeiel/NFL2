setwd("~/Python/NFL2/DATA/R")

library(nflscrapR)
ids = scrape_game_ids(2019)
week = 1 

week_games = ids[ids$week==week,]
pbp = data.frame()
for (game in week_games$game_id){
pbp = rbind(pbp, scrape_game_play_by_play(game, 'reg', 2019))
}

write.csv(pbp, '../play_by_play_data/regular_season/reg_pbp_2019.csv')
