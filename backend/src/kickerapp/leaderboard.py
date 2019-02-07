from flask_restful import Resource, reqparse
from .view_models import LeaderboardViewModel


class LeaderboardResource(Resource):
    def get(self):
        return LeaderboardViewModel().serialize()
