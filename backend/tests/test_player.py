from datetime import datetime
import sys
sys.path.append('../src')

from base import KickerTest, KickerTestWithFixtures
from kickerapp.config import *


class TestPlayers(KickerTestWithFixtures):
    """
    Tests /player and /players endpoints.
    Also tests the Slack integration since it's used as a fixture.
    """
    def test_get_list_of_players(self):
        response = self.client.get("/kickerscore/api/v2/players")

        assert response.status_code == 200

        data = response.json

        assert data['players'] is not None
        assert len(data['players']) > 0

        for player in data['players']:
            assert type(player['username']) is str
            assert type(player['avatar']) is str

    def test_get_player(self):
        response = self.client.get("/kickerscore/api/v2/player?username=steven")

        assert response.status_code == 200

        data = response.json
        player = data['player']

        assert player is not None
        assert player['username'] == "steven"
        assert type(player['avatar']) is str
        assert type(player['registration_date']) is str
        assert datetime.strptime(player['registration_date'], '%Y-%m-%d %H:%M:%S.%f')

        assert player['current_rank']['overall'] is None or type(player['current_rank']['overall']) is int
        assert player['current_rank']['offense'] is None or type(player['current_rank']['offense']) is int
        assert player['current_rank']['defense'] is None or type(player['current_rank']['defense']) is int

        self.assertAlmostEqual(player['current_mu']['overall'], MU)
        self.assertAlmostEqual(player['current_mu']['offense'], MU)
        self.assertAlmostEqual(player['current_mu']['defense'], MU)

        self.assertAlmostEqual(player['current_sigma']['overall'], SIGMA)

        self.assertAlmostEqual(player['current_sigma']['offense'], SIGMA)
        self.assertAlmostEqual(player['current_sigma']['defense'], SIGMA)

        self.assertAlmostEqual(player['current_rating']['overall'], MU - (3 * SIGMA))
        self.assertAlmostEqual(player['current_rating']['offense'], MU - (3 * SIGMA))
        self.assertAlmostEqual(player['current_rating']['defense'], MU - (3 * SIGMA))

        assert type(data['rating_over_time']) is dict
