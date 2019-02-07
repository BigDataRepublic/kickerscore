from datetime import datetime
import json
import sys
sys.path.append('../src')

from base import KickerTestWithFixtures
from kickerapp.config import *
from kickerapp.models import Player
from app import db


class TestAnalysis(KickerTestWithFixtures):
    """
    Tests analyzing players and teams.
    """
    def test_fair_matchup(self):
        # Grab the Player objects of 4 players
        players = Player.query.order_by(Player.slack_username).limit(4)

        # Set custom ratings
        # medium defense, bad offense
        players[0].rating_mu = 800
        players[0].rating_mu_offense = 800
        players[0].rating_mu_defense = 1000
        players[0].rating_sigma = 150
        players[0].rating_sigma_offense = 100
        players[0].rating_sigma_defense = 200

        # good defense, medium offense
        players[1].rating_mu = 1200
        players[1].rating_mu_offense = 1000
        players[1].rating_mu_defense = 1200
        players[1].rating_sigma = 150
        players[1].rating_sigma_offense = 200
        players[1].rating_sigma_defense = 100

        # medium defense, bad offense
        players[2].rating_mu = 800
        players[2].rating_mu_offense = 800
        players[2].rating_mu_defense = 1000
        players[2].rating_sigma = 150
        players[2].rating_sigma_offense = 100
        players[2].rating_sigma_defense = 200

        # good defense, medium offense
        players[3].rating_mu = 1200
        players[3].rating_mu_offense = 1000
        players[3].rating_mu_defense = 1200
        players[3].rating_sigma = 150
        players[3].rating_sigma_offense = 200
        players[3].rating_sigma_defense = 100

        db.session.commit()

        data = {
            "players": [players[0].slack_username, players[1].slack_username, players[2].slack_username, players[3].slack_username],
            "best_match_only": True
        }

        # Analyze the matchup
        response = self.client.post("/kickerscore/api/v2/analyze-players", data=data)
        assert response.status_code == 200

        json = response.json

        self.assertAlmostEqual(json['predicted_win_prob_for_blue'], 0.5)
        self.assertAlmostEqual(json['match_balance'], 0.6401843996644798)

        assert json['optimal_team_composition']['blue']['offense'] == players[0].slack_username
        assert json['optimal_team_composition']['blue']['defense'] == players[1].slack_username
        assert json['optimal_team_composition']['red']['offense'] == players[2].slack_username
        assert json['optimal_team_composition']['red']['defense'] == players[3].slack_username
