from flask import jsonify

from . import api

@api.route("/health-check")
def health_check():
    return jsonify({"message": "success"}), 200