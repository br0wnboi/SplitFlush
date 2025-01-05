import requests
from tabulate import tabulate

# The correct URL without the fragment part
POKERNOW_URL = "https://www.pokernow.club/games/pglLh4W45YB7IFI4Zr4QfPgo0/players_sessions"
HEADERS = {
    "cookie": "aws-waf-token=6f0c3a1e-fe0a-405e-83a7-555cd31e052b:EQoAfZpot7nfAAAA:xqtMEwSSv8FFMbBOFYD8s4+zIFfJEcgCc5+wmoffi8eh3QiCh6K4kz2xH9rMt3X/CozRhxU8WJwlQ2SLuPoWxdniYpJqDeVf4+k75oocCjx+kjDXQZuj6ufwLS9LU5kUkPZPp0PpIp7R07xAs5q/JDnzAHK+NBL81Jk3wf197EMUq/vUUqCVDQgUzR6qYrF1VBktOWAKfMAN"
}
# Ensure the URL ends with '/player_sessions'
if not POKERNOW_URL.endswith('/players_sessions'):
    POKERNOW_URL += '/players_sessions'

def fetch_game_data(url, headers):
    """Fetch game data from PokerNow."""
    try:
        # Fetch the game data from the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx

        # Check if the response is in JSON format, otherwise print response text
        try:
            return response.json()
        except ValueError:
            print(f"Error: Response is not in JSON format.\nResponse Text: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_game_data(game_data):
    """Parse game data to extract player information."""
    if "playersInfos" not in game_data:
        print("Error: 'playersInfos' key not found in the game data.")
        return []

    table_data = []
    for player_id, player_info in game_data["playersInfos"].items():
        table_data.append([
            player_info["names"][0] if "names" in player_info and player_info["names"] else "Unknown",
            player_info.get("buyInSum", 0),
            player_info.get("buyOutSum", 0),
            player_info.get("inGame", 0),
            player_info.get("net", 0),
        ])
    return table_data

def main():
    """Main function to fetch, parse, and display game data."""
    game_data = fetch_game_data(POKERNOW_URL, HEADERS)
    if not game_data:
        print("Failed to retrieve game data. Exiting...")
        return

    table_data = parse_game_data(game_data)
    if table_data:
        headers = ["Player Name", "Total Buy-In", "Total Buy-Out", "In Game", "Net"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("No player data to display.")

if __name__ == "__main__":
    main()
