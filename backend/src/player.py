from flask_restful import Resource, reqparse
from models import Player
from config import *
from datetime import datetime
from db import db


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

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)

        args = parser.parse_args()

        # Check if player already exists
        if Player.query.filter_by(username=args['username']).count() > 0:
            return "Player already exists", 409

        player = Player()
        player.username = args['username']
        player.rating_mu = MU
        player.rating_mu_offense = MU
        player.rating_mu_defense = MU
        player.rating_sigma = SIGMA
        player.rating_sigma_offense = SIGMA
        player.rating_sigma_defense = SIGMA
        player.registration_date = datetime.utcnow()

        db.session.add(player)
        db.session.commit()

        return "OK", 200
