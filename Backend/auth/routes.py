from flask import Blueprint, request, jsonify
from app import db
from db.models import User 
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# Register route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({"message": "Email already registered"}), 400

    user = User(email=data.get("email"),name=data.get("name"))
    user.set_password(data.get("password"))

    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": "Registration failed"}), 500
    return jsonify({"message": "User created successfully"}), 201


# Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not user.check_password(data.get("password")):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "Logged in successfully", "token": access_token}), 200

@auth_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200