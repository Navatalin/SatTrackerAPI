from flask import Flask, jsonify
from flask_restful import Resource, Api
from Tracking import Tracking

app = Flask(__name__)
api = Api(app)
track = Tracking()
class SatelliteQuery(Resource):
    def get(self):
        result = track.get_pos()
        return jsonify(result)

api.add_resource(SatelliteQuery, '/')

if __name__ == '__main__':
    app.run()