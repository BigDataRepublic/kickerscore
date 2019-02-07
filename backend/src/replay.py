# Run this file to import an existing CSV file with matches into the database, recalculating all ratings.
# CSV file format:
# Line 1: Header
# Columns: blue_offense_player,blue_defense_player,red_offense_player,red_defense_player,blue_points,red_points
import pandas as pd
import requests
import json


class Replay():
    def __init__(self, csv_file):
        self.file = csv_file

    def start(self):
        # Read file
        matches = pd.read_csv(self.file)

        # Get all players so we can convert id to username
        players = requests.get("http://localhost:5000/kickerscore/api/v2/players")
        id_dict = {}
        for p in players.json()["players"]:
            id_dict[p['slack_id']] = p['username']

        # Loop through list, insert new matches for every row
        for _, match in matches.iterrows():
            if match['blue_offense_player'] in id_dict and match['blue_defense_player'] in id_dict and match['red_offense_player'] in id_dict and match['red_defense_player'] in id_dict:
                payload = {
                    "players": json.dumps({
                        "blue": {
                            "offense": id_dict[match['blue_offense_player']],
                            "defense": id_dict[match['blue_defense_player']]
                        },
                        "red": {
                            "offense": id_dict[match['red_offense_player']],
                            "defense": id_dict[match['red_defense_player']]
                        }}),
                    "points": json.dumps({
                        "blue": match['blue_points'],
                        "red": match['red_points']
                    })}
                requests.post("http://localhost:5000/kickerscore/api/v2/match", data=payload)
            else:
                print("Missing player row, skipping match")


if __name__ == '__main__':
    r = Replay("export.csv")
    r.start()
