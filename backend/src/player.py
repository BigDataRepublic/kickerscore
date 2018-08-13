from flask_restful import Resource, reqparse
from models import Player


class PlayersResource(Resource):
    def get(self):
        return list(map(lambda x: x.serialize(), Player.query.all()))


class PlayerResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)

        args = parser.parse_args()

        player = Player.query.filter_by(username=args['username']).first()

        if player is None:
            return f"Player with username {args['username']} not found", 404

        return player.serialize()
