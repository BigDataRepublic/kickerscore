from flask_restful import Resource, reqparse
from models import Player


class PlayersResource(Resource):
    def get(self):
        players = Player.query.filter_by(active=True)
        players = filter(lambda x: x.num_matches > 0, players)
        return list(map(lambda x: x.serialize(), players))


class PlayerResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)

        args = parser.parse_args()
        username = args['username'].lower()

        player = Player.query.filter_by(username=username).first()

        if player is None:
            return f"Player with username {username} not found", 404

        return player.serialize()
