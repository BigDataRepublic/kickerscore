import atexit
from flask import Flask
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.contrib.profiler import ProfilerMiddleware

from kickerapp.match import MatchResource, MatchesResource, AnalyzePlayers, AnalyzeTeams
from kickerapp.player import PlayerResource, PlayersResource
from kickerapp.leaderboard import LeaderboardResource
from kickerapp.face import FaceRecognitionResource, AddFacesResource
from kickerapp.db import *
from kickerapp.slack_sync import sync_new_and_left_channel_members, sync_existing_members_info


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
cors = CORS(app)
db.init_app(app)
db.app = app

migrate = Migrate(app, db)

# Profiler
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir="./perf_test/")

# Watch it: this stuff will get out of control if you run multiple
# instances of this app. Need to ensure there's just one scheduler!
scheduler = BackgroundScheduler(timezone="Europe/Amsterdam")
# Check channel if there are new players
new_player_sync = scheduler.add_job(sync_new_and_left_channel_members, "interval", minutes=5)
# Revisit existing players and update info if changed
existing_player_sync = scheduler.add_job(sync_existing_members_info, "interval", minutes=10)


class Healthz(Resource):
    """
    Resource check for Kubernetes.
    """
    def get(self):
        return "OK", 200


api.add_resource(MatchesResource, '/kickerscore/api/v2/matches')
api.add_resource(MatchResource, '/kickerscore/api/v2/match')
api.add_resource(PlayersResource, '/kickerscore/api/v2/players')
api.add_resource(LeaderboardResource, '/kickerscore/api/v2/leaderboard')
api.add_resource(PlayerResource, '/kickerscore/api/v2/player')
api.add_resource(AnalyzePlayers, '/kickerscore/api/v2/analyze-players')
api.add_resource(AnalyzeTeams, '/kickerscore/api/v2/analyze-teams')
api.add_resource(FaceRecognitionResource, '/kickerscore/api/v2/recognize-faces')
api.add_resource(AddFacesResource, '/kickerscore/api/v2/add-faces')
api.add_resource(Healthz, '/healthz')

if __name__ == '__main__':
    scheduler.start()
    new_player_sync.func()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    app.run(debug=False, host="0.0.0.0", port=5000, threaded=True)
