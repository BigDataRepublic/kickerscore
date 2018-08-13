from flask_restful import Resource, reqparse
from models import Match
import analysis
from models import Player


class MatchesResource(Resource):
    def get(self):
        return list(map(lambda x: x.serialize(), Match.query.limit(100).all()))


class MatchResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)

        args = parser.parse_args()

        match = Match.query.filter_by(id=args['id']).first()

        if match is None:
            return f"Match with id {args['id']} not found", 404

        return match.serialize()

    def post(self):
        return "OK", 200


class AnalyzePlayers(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('players', type=str, action='append')

        args = parser.parse_args()

        players = list(map(lambda x: Player.query.filter_by(username=x).first(), args['players']))
        stats = analysis.analyze_players(players)

        return stats


class AnalyzeTeams(Resource):
    def get(self):
        return "OK", 200
