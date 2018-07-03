from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from match import Match, Matches, MatchPredict
from player import Player, Players


app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)


class Healthz(Resource):
    """
    Resource check for Kubernetes.
    """
    def get(self):
        return "OK", 200


api.add_resource(Matches, '/kickerscore/api/v1/matches')
api.add_resource(Match, '/kickerscore/api/v1/match')
api.add_resource(Players, '/kickerscore/api/v1/players')
api.add_resource(Player, '/kickerscore/api/v1/player')
api.add_resource(MatchPredict, '/kickerscore/api/v1/match_predict')
api.add_resource(Healthz, '/healthz')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
