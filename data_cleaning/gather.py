import pandas as pd
import requests
from bs4 import BeautifulSoup

espn_teams = ['BAL', 'PHI', 'ARI', 'CHI', 'JAX', 'NO', 'SF', 'LAR', 'CAR', 'PIT', 'HOU', 'DEN', 'CIN', 'IND',
              'NYG', 'WSH', 'DAL', 'TB', 'SEA', 'ATL', 'KC', 'LAC', 'MIN', 'NE', 'CLE', 'BUF', 'TEN', 'GB',
              'NYJ', 'OAK', 'MIA', 'DET']

team_to_team = {'ARI': 'ARI', 'ATL': 'ATL', 'BAL': 'BAL', 'BUF': 'BUF', 'CAR': 'CAR', 'CHI': 'CHI', 'CIN': 'CIN',
                'CLE': 'CLE', 'DAL': 'DAL', 'DEN': 'DEN', 'DET': 'DET', 'GB': 'GB', 'HOU': 'HOU', 'IND': 'IND',
                'JAX': 'JAX', 'KC': 'KC', 'LAC': 'LA', 'LAR': 'LAC', 'MIA': 'MIA', 'MIN': 'MIN', 'NE': 'NE',
                'NO': 'NO', 'NYG': 'NYG', 'NYJ': 'NYJ', 'OAK': 'OAK', 'PHI': 'PHI', 'PIT': 'PIT', 'SEA': 'SEA',
                'SF': 'SF', 'TB': 'TB', 'TEN': 'TEN', 'WSH': 'WAS'}


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

def get_lines():
    res = requests.get('http://www.espn.com/nfl/lines')
    soup = BeautifulSoup(res.content, 'html.parser')
    table = soup.find('table')
    # need to grab Ceasar's line for each game and save the values in lists
    # then save to a dataframe
    rows = table.find_all('tr')
    ceasars = [row for row in rows if row.find('td').text == 'Caesars']

    week = soup.find('h1').text.strip().split('Week')[-1]

    home_spread = [game.find('table').find_all('br')[0].next_sibling for game in ceasars]
    home_odds = [game.find('table').find_all('br')[1].next_sibling for game in ceasars]
    home_team = [team.split(':')[0] for team in home_odds]

    away_spread = [game.find('table').find_all('br')[0].previous_sibling for game in ceasars]
    away_odds = [game.find('table').find_all('br')[1].previous_sibling for game in ceasars]
    away_team = [team.split(':')[0] for team in away_odds]

    df = pd.DataFrame(data={'week':week, 'ceasars_home_spread':home_spread, 'home_odds':home_odds,
                            'ceasars_away_spread':away_spread, 'away_odds':away_odds,
                            'home_team':home_team, 'away_team':away_team})
    df.home_team.replace(team_to_team, inplace=True)
    df.away_team.replace(team_to_team, inplace=True)

    return df