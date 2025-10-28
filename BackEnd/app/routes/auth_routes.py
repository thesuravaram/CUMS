# from flask import Blueprint, request, jsonify
# from app.services.auth_service import register_user, login_user

# auth_bp = Blueprint("auth", __name__)

# @auth_bp.route("/register", methods=["POST"])
# def register():
#     data = request.json
#     return register_user(data["email"], data["password"],data['role'])

# @auth_bp.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     return login_user(data["email"], data["password"])


from flask import Blueprint, request
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    return register_user(data["email"],data["password"],data.get("role", "student"))

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    print(data)
    return login_user(data["email"],data["password"])
