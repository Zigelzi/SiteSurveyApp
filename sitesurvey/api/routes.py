from flask import Blueprint, jsonify, request
from sitesurvey import ma

from sitesurvey.user.models import Organization
from sitesurvey.survey.models import Location

bp_api = Blueprint('api', __name__)

# Marshmallow schemas for serializing the DB queries to JSON objects

class LocationSchema(ma.ModelSchema):
    class Meta:
        # Fields which will be exposed to serialization
        model = Location

class CustomerSchema(ma.ModelSchema):
    class Meta:
        model = Organization

class OrganizationSchema(ma.ModelSchema):
    class Meta:
        model = Organization

@bp_api.route('/api/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    location_schema = LocationSchema(many=True)
    output = location_schema.dump(locations).data
    print(output)
    return jsonify(output)

@bp_api.route('/api/customers', methods=['GET'])
def get_customers():
    organizations = Organization.query.all()
    customers = []

    # Append all the organizations that have org_type of 'Customer' to customers list
    for org in organizations:
        for org_type in org.org_type:
            if org_type.title == 'Customer':
                customers.append(org)
    
    customer_schema = CustomerSchema(many=True)
    output = customer_schema.dump(customers).data
    print(output)
    return jsonify(output)

@bp_api.route('/api/organizations', methods=['GET'])
def get_organizations():
    organizations = Organization.query.all()
    organization_schema = OrganizationSchema(many=True)
    output = organization_schema.dump(organizations).data
    print(output)
    return jsonify(output)