from flask_restful import Resource, reqparse
from models import Player


class PlayersResource(Resource):
    def get(self):
        return Player.query.all()


class PlayerResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)

        args = parser.parse_args()

        return Player.query.filter_by(username=args['username']).first()
