import pandas as pd
from time import sleep
from lib import BRASILEIRAO_ID, get_clubs, get_player_stats, get_players, safe_list_get

if __name__ == "__main__":
    clubs = get_clubs(BRASILEIRAO_ID)
    
    all_players = []
    
    for club in clubs:
        sleep(1)  # Evitar rate limiting
        print(f"Processando {club['name']}...")
        
        try:
            players = get_players(club['id'])
            for player in players:
                sleep(1)  # Evitar rate limiting
                print(f"Processando {player['name']}...")
                all_stats = get_player_stats(player['id'])
                stat = [stat for stat in all_stats if stat['competitionId'] == BRASILEIRAO_ID and stat['seasonId'] == '2024']
                brasileirao_2024 = safe_list_get(stat, 0, {})

                player_data = {
                    'nome': player.get('name', ''),
                    'posicao': player.get('position', ''),
                    'idade': player.get('age', ''),
                    'nacionalidade': safe_list_get(player.get('nationality', []), 0, ''),
                    'valor de mercado': player.get('marketValue', ''),
                    'clube': club['name'],
                    'altura': player.get('height', ''),
                    'pe dominante': player.get('foot', ''),
                    'contrato': player.get('contract', ''),
                    'clube anterior': player.get('signedFrom', ''),
                    'partidas': brasileirao_2024.get('appearances', 0),
                    'gols': brasileirao_2024.get('goals', 0),
                    'assistencias': brasileirao_2024.get('assists', 0),
                    'cartoes amarelos': brasileirao_2024.get('yellowCards', 0),
                    'minutos jogados': brasileirao_2024.get('minutesPlayed', 0)
                }
                print(player_data)
                all_players.append(player_data)
        except Exception as e:
            print(f"Erro no clube {club['name']}: {e}")
    
    df = pd.DataFrame(all_players)
    df.to_csv('brasileirao_2024.csv', index=False, encoding='utf-8-sig')
    print("CSV criado com sucesso!")