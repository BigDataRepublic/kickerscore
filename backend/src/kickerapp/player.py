from flask_restful import Resource, reqparse
from .view_models import AddMatchPlayerListViewModel, PlayerInformationViewModel


class PlayersResource(Resource):
    def get(self):
        return AddMatchPlayerListViewModel().serialize()


class PlayerResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)

        args = parser.parse_args()
        username = args['username'].lower()

        player_view_model = PlayerInformationViewModel(username=username)

        if not player_view_model.exists():
            return f"Player with username {username} not found", 404

        return player_view_model.serialize()
