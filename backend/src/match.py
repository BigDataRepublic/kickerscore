from flask_restful import Resource, reqparse
from models import Match


class MatchesResource(Resource):
    def get(self):
        return Match.query.limit(100).all()


class MatchResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)

        args = parser.parse_args()

        return Match.query.filter_by(id=args['id']).first()

    def post(self):
        return "OK", 200


class AnalyzePlayers(Resource):
    def get(self):
        return "OK", 200

class AnalyzeTeams(Resource):
    def get(self):
        return "OK", 200
