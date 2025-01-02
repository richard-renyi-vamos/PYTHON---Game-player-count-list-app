import requests
import time

# Function to get the list of top games from Steam
# Note: Replace 'YOUR_STEAM_API_KEY' with your actual Steam API key
def get_top_games(api_key):
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch game list")
        return []

    games = response.json()['applist']['apps']
    return games

# Function to get player count for a specific game
def get_player_count(api_key, app_id):
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?key={api_key}&appid={app_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return data.get('response', {}).get('player_count', 0)

# Main function to fetch the top 500 games by player count
def fetch_top_500_games():
    API_KEY = "YOUR_STEAM_API_KEY"
    games = get_top_games(API_KEY)
    
    if not games:
        return

    game_player_counts = []

    for game in games[:500]:
        app_id = game['appid']
        name = game['name']
        player_count = get_player_count(API_KEY, app_id)

        if player_count is not None:
            game_player_counts.append((name, player_count))

        # Respect API rate limits
        time.sleep(0.1)

    # Sort games by player count in descending order
    game_player_counts.sort(key=lambda x: x[1], reverse=True)

    for rank, (name, player_count) in enumerate(game_player_counts[:500], start=1):
        print(f"{rank}. {name}: {player_count} players")

if __name__ == "__main__":
    fetch_top_500_games()
