import pandas as pd
import requests
from bs4 import BeautifulSoup

espn_teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN',
              'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC', 'LAC', 'LAR', 'MIA', 'MIN', 'NE',
              'NO', 'NYG', 'NYJ', 'OAK', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH']


# takes care of ESPN/R discrepancies in team names: LAR -> LA ; WSH -> WAS
team_to_team = {'ARI': 'ARI', 'ATL': 'ATL', 'BAL': 'BAL', 'BUF': 'BUF', 'CAR': 'CAR', 'CHI': 'CHI', 'CIN': 'CIN',
                'CLE': 'CLE', 'DAL': 'DAL', 'DEN': 'DEN', 'DET': 'DET', 'GB': 'GB', 'HOU': 'HOU', 'IND': 'IND',
                'JAX': 'JAX', 'KC': 'KC', 'LAC': 'LAC', 'LAR': 'LA', 'MIA': 'MIA', 'MIN': 'MIN', 'NE': 'NE',
                'NO': 'NO', 'NYG': 'NYG', 'NYJ': 'NYJ', 'OAK': 'OAK', 'PHI': 'PHI', 'PIT': 'PIT', 'SEA': 'SEA',
                'SF': 'SF', 'TB': 'TB', 'TEN': 'TEN', 'WSH': 'WAS'}

def get_lines():
    res = requests.get('http://www.espn.com/nfl/lines')
    soup = BeautifulSoup(res.content, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    westgate = [row for row in rows if row.find('td').text == 'Westgate']

    week = soup.find('h1').text.strip().split('Week')[-1]

    home_spread = [game.find('table').find_all('br')[0].next_sibling for game in westgate]
    home_odds = [game.find('table').find_all('br')[1].next_sibling for game in westgate]
    home_team = [team.split(':')[0] for team in home_odds]

    away_spread = [game.find('table').find_all('br')[0].previous_sibling for game in westgate]
    away_odds = [game.find('table').find_all('br')[1].previous_sibling for game in westgate]
    away_team = [team.split(':')[0] for team in away_odds]

    df = pd.DataFrame(data={'week' : int(week), 'vegas_line_home' : home_spread, 'home_odds' : home_odds,
                            'vegas_line_away' : away_spread, 'away_odds' : away_odds,
                            'home_team' : home_team, 'away_team' : away_team})
    df.home_team.replace(team_to_team, inplace=True)
    df.away_team.replace(team_to_team, inplace=True)

    return df
