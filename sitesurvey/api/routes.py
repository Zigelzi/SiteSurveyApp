from flask import Blueprint, jsonify, request
from sitesurvey import ma

from sitesurvey.user.models import Organization, Contactperson
from sitesurvey.survey.models import Location
from sitesurvey.product.models import Product

bp_api = Blueprint('api', __name__)

# Marshmallow schemas for serializing the DB queries to JSON objects

class LocationSchema(ma.ModelSchema):
    class Meta:
        # Fields which will be exposed to serialization
        model = Location

class CustomerSchema(ma.ModelSchema):
    class Meta:
        model = Organization

class ContactPersonSchema(ma.ModelSchema):
    class Meta:
        model = Contactperson

class OrganizationSchema(ma.ModelSchema):

    contact_persons = ma.Nested(ContactPersonSchema, many=True)

    class Meta:
        model = Organization

class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product

@bp_api.route('/api/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    location_schema = LocationSchema(many=True)
    output = location_schema.dump(locations).data
    print(output)
    return jsonify(output)

@bp_api.route('/api/location/<string:location_name>', methods=['GET'])
def get_location(location_name):
    location = Location.query.filter_by(name=location_name).first()
    location_schema = LocationSchema()
    output = location_schema.dump(location).data
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

@bp_api.route('/api/organization/<string:org_name>', methods=['GET'])
def get_organization(org_name):
    organization = Organization.query.filter_by(org_name=org_name).first()
    organization_schema = OrganizationSchema()
    output = organization_schema.dump(organization).data
    print(output)
    return jsonify(output)

@bp_api.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products).data
    print(output)
    return jsonify(output)

@bp_api.route('/api/product/<string:product_number>', methods=['GET'])
def get_product(product_number):
    product = Product.query.filter_by(product_number=product_number).first()
    product_schema = ProductSchema()
    output = product_schema.dump(product).data
    print(output)
    return jsonify(output)