from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from match import MatchResource, MatchesResource, AnalyzePlayers, AnalyzeTeams
from player import PlayerResource, PlayersResource
from db import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
cors = CORS(app)
db.init_app(app)

migrate = Migrate(app, db)


class Healthz(Resource):
    """
    Resource check for Kubernetes.
    """
    def get(self):
        return "OK", 200



api.add_resource(MatchesResource, '/kickerscore/api/v1/matches')
api.add_resource(MatchResource, '/kickerscore/api/v1/match')
api.add_resource(PlayersResource, '/kickerscore/api/v1/players')
api.add_resource(PlayerResource, '/kickerscore/api/v1/player')
api.add_resource(AnalyzePlayers, '/kickerscore/api/v1/analyze-players')
api.add_resource(AnalyzeTeams, '/kickerscore/api/v1/analyze-teams')
api.add_resource(Healthz, '/healthz')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
