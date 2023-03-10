from typing import Optional

from flask import jsonify, request
from marshmallow.exceptions import ValidationError

from app.schema import OwnerCarSchema
from tools.auth import auth, token_required

from . import api


@api.route("/health-check", methods=["GET"])
def health_check():
    return jsonify({"message": "success"}), 200


@api.route("/api/login", methods=["POST"])
def login():
    return auth()


@api.route("/api/car", methods=["POST"])
@token_required
def car(current_user):
    data: dict = request.get_json()
    try:
        schema: Optional[dict] = OwnerCarSchema().load(data)
        if schema is None:
            response_json = {
                "error_message": "It was not possible to validate the sent data, invalid data"
            }
            return jsonify(response_json), 400
    except ValidationError as error:
        response_json = error.normalized_messages()
        return jsonify(response_json), 400
    return jsonify({"message": "success"}), 201
