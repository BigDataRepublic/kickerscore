from datetime import datetime
import json
import sys
sys.path.append('../src')

from base import KickerTest, KickerTestWithFixtures
from kickerapp.config import *
from kickerapp.models import Player


class TestMatches(KickerTestWithFixtures):
    """
    Tests creating a new match and retrieving it.
    """
    def test_get_empty_list_of_matches(self):
        response = self.client.get("/kickerscore/api/v2/matches")

        assert response.status_code == 200

        data = response.json
        matches = data['matches']

        assert type(matches) is list
        assert len(matches) == 0

    def test_post_match(self):
        # First, we test whether currently there are no matches in the database
        self.test_get_empty_list_of_matches()

        # Grab the Player objects of 4 players
        players = Player.query.order_by(Player.slack_username).limit(4)

        data = {
            "players": json.dumps({
                "blue": {
                    "offense": players[0].slack_username,
                    "defense": players[1].slack_username
                },
                "red": {
                    "offense": players[2].slack_username,
                    "defense": players[3].slack_username
                }
            }),
            "points": json.dumps({
                "blue": 10,
                "red": 6
            })
        }

        ratings_before = list(map(lambda x: x.rating_mu, players))
        ratings_offense_before = list(map(lambda x: x.rating_mu_offense, players))
        ratings_defense_before = list(map(lambda x: x.rating_mu_defense, players))

        sigma_before = list(map(lambda x: x.rating_sigma, players))
        sigma_offense_before = list(map(lambda x: x.rating_sigma_offense, players))
        sigma_defense_before = list(map(lambda x: x.rating_sigma_defense, players))

        # Create the match
        response = self.client.post("/kickerscore/api/v2/match", data=data)
        assert response.status_code == 200

        # Check whether the ratings of the players changed
        updated_players = Player.query.order_by(Player.slack_username).limit(4)

        ratings_after = list(map(lambda x: x.rating_mu, updated_players))
        ratings_offense_after = list(map(lambda x: x.rating_mu_offense, updated_players))
        ratings_defense_after = list(map(lambda x: x.rating_mu_defense, updated_players))

        sigma_after = list(map(lambda x: x.rating_sigma, updated_players))
        sigma_offense_after = list(map(lambda x: x.rating_sigma_offense, updated_players))
        sigma_defense_after = list(map(lambda x: x.rating_sigma_defense, updated_players))

        assert ratings_after[0] > ratings_before[0]
        assert ratings_after[1] > ratings_before[1]
        assert ratings_after[2] < ratings_before[2]
        assert ratings_after[3] < ratings_before[3]

        assert ratings_offense_after[0] > ratings_offense_before[0]
        self.assertAlmostEqual(ratings_offense_after[1], ratings_offense_before[1])
        assert ratings_offense_after[2] < ratings_offense_before[2]
        self.assertAlmostEqual(ratings_offense_after[3], ratings_offense_before[3])

        self.assertAlmostEqual(ratings_defense_after[0], ratings_defense_before[0])
        assert ratings_defense_after[1] > ratings_defense_before[1]
        self.assertAlmostEqual(ratings_defense_after[2], ratings_defense_before[2])
        assert ratings_defense_after[3] < ratings_offense_before[3]

        assert sigma_after[0] < sigma_before[0]
        assert sigma_after[1] < sigma_before[1]
        assert sigma_after[2] < sigma_before[2]
        assert sigma_after[3] < sigma_before[3]

        assert sigma_offense_after[0] < sigma_offense_before[0]
        self.assertAlmostEqual(sigma_offense_after[1], sigma_offense_before[1])
        assert sigma_offense_after[2] < sigma_offense_before[2]
        self.assertAlmostEqual(sigma_offense_after[3], sigma_offense_before[3])

        self.assertAlmostEqual(sigma_defense_after[0], sigma_defense_before[0])
        assert sigma_defense_after[1] < sigma_defense_before[1]
        self.assertAlmostEqual(sigma_defense_after[2], sigma_defense_before[2])
        assert sigma_defense_after[3] < sigma_defense_before[3]

        self._test_get_match()

    def _test_get_match(self):
        response = self.client.get("/kickerscore/api/v2/matches")

        assert response.status_code == 200

        data = response.json
        matches = data['matches']

        assert type(matches) is list
        assert len(matches) == 1
