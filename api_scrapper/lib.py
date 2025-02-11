import requests

API_BASE = "https://transfermarkt-api.fly.dev"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

BRASILEIRAO_ID = "BRA1"

def get_clubs(competition_id):
    url = f"{API_BASE}/competitions/{competition_id}/clubs"
    response = requests.get(url, headers=HEADERS)
    return response.json()['clubs']

def get_players(club_id):
    url = f"{API_BASE}/clubs/{club_id}/players"
    response = requests.get(url, headers=HEADERS)
    players = response.json()['players']
    return [player for player in players if player['position'] != "Goalkeeper"]

def get_player_stats(player_id):
    url = f"{API_BASE}/players/{player_id}/stats"
    response = requests.get(url, headers=HEADERS)
    return response.json()['stats']

def safe_list_get (l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default