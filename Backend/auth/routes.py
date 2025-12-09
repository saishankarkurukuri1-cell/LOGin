from flask import Blueprint, request, jsonify
from app import db
from database.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# Register route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({"msg": "Email already registered"}), 400

    user = User(email=data.get("email"))
    user.set_password(data.get("password"))

    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201


# Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not user.check_password(data.get("password")):
        return jsonify({"msg": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"msg": "Logged in successfully", "token": access_token}), 200