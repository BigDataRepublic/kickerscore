from flask_restful import Resource


class Players(Resource):
    def get(self):
        return "OK", 200


class Player(Resource):
    def get(self):
        return "OK", 200
