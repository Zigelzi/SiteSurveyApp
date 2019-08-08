from flask import Blueprint, jsonify, request
from sitesurvey import ma
from sitesurvey.survey.models import Location

bp_api = Blueprint('api', __name__)

# Marshmallow schemas for serializing the DB queries to JSON objects

class LocationSchema(ma.ModelSchema):
    class Meta:
        # Fields which will be exposed to serialization
        model = Location


@bp_api.route('/api/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    location_schema = LocationSchema(many=True)
    output = location_schema.dump(locations).data
    print(output)
    return jsonify(output)
