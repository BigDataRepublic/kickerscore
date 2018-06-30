from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Match(Resource):
    def get(self):
        return {"hello": "world"}

api.add_resource(Match, '/kickerscore/api/v1/match')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
