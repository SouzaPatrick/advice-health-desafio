from flask import jsonify, request
from typing import Optional
from marshmallow.exceptions import ValidationError
from app.schema import OwnerCarSchema

from . import api

@api.route("/health-check", methods=["GET"])
def health_check():
    return jsonify({"message": "success"}), 200

@api.route("/api/car", methods=["POST"])
def car():
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
    return jsonify({"message": "success"}), 200