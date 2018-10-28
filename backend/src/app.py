import atexit

from flask import Flask
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

from match import MatchResource, MatchesResource, AnalyzePlayers, AnalyzeTeams
from player import PlayerResource, PlayersResource
from db import *
from slack_sync import sync_new_left_channel_members, sync_existing_members_info


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
app.config['SQLALCHEMY_TRAdCK_MODIFICATIONS'] = False
api = Api(app)
cors = CORS(app)
db.init_app(app)
db.app = app

migrate = Migrate(app, db)

# Watch it: this stuff will get out of control if you run multiple
# instances of this app. Need to ensure there's just one scheduler!
scheduler = BackgroundScheduler(timezone="Europe/Amsterdam")
# Check channel if there are new players
new_player_sync = scheduler.add_job(sync_new_left_channel_members, "interval", seconds=30)
# Revisist existing players and update info if required
existing_player_sync = scheduler.add_job(sync_existing_members_info, "interval", minutes=1)
scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


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
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=True)
