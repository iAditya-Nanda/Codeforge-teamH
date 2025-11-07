from flask import Blueprint, request
from controllers.auth_controller import signup_user, login_user

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data:
        return {"error": "Invalid or missing JSON body"}, 400
    return signup_user(data)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return {"error": "Invalid or missing JSON body"}, 400
    return login_user(data)
