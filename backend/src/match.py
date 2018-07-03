from flask_restful import Resource


class Matches(Resource):
    def get(self):
        return "OK", 200


class Match(Resource):
    def get(self):
        return "OK", 200

    def post(self):
        return "OK", 200

    def patch(self):
        return "OK", 200


class MatchPredict(Resource):
    def get(self):
        return "OK", 200
