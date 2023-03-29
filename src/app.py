"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/test', methods=['GET'])
def handle_test():
    response_body = {
        "message": "This is a test endpoint"
    }
    return jsonify(response_body), 200

@app.route('/members', methods=['GET'])
def handle_get_all_members():
    # retrieve all family members from the jackson_family object
    members = jackson_family.get_all_members()

    # create a response body with the list of members
    response_body = members

    # return the response body as a JSON object with a 200 OK status code
    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    # retrieve the member with the given ID from the jackson_family object
    member = jackson_family.get_member(id)

    # if no member with the given ID is found, return a 404 Not Found error
    if not member:
        response_body = {
            "error": "Member not found"
        }
        return jsonify(response_body), 404

    # create a response body with the member's information
    response_body = {
        "id": member["id"],
        "first_name": member["first_name"],
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    }

    # return the response body as a JSON object with a 200 OK status code
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def handle_add_member():
    # retrieve the request body as a JSON object
    request_body = request.get_json()

    # validate the request body and create a new member dictionary
    new_member = {
        "first_name": request_body.get("first_name"),
        "age": request_body.get("age"),
        "lucky_numbers": request_body.get("lucky_numbers"),
        "id": request_body.get("id")
    }

    # add the new member to the jackson_family object
    jackson_family.add_member(new_member)

    # return an empty response with a 200 OK status code
    return jsonify({}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    # delete the member with the given ID from the jackson_family object
    deleted = jackson_family.delete_member(member_id)

    # if no member with the given ID is found, return a 404 Not Found error
    if not deleted:
        response_body = {
            "error": "Member not found"
        }
        return jsonify(response_body), 404

    # create a response body with the "done" flag set to True
    response_body = {
        "done": True
    }

    # return the response body as a JSON object with a 200 OK status code
    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
