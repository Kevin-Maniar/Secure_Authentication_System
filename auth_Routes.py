# ------  Login And Registration Routes

from flask import Blueprint, request, jsonify
from User_model import db, User
import bcrypt
import jwt
import datetime

auth_bp = Blueprint("auth", __name__)

# JWT config
JWT_SECRET = "supersecretkey"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

# --------- Registration --------- #
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Please provide name, email, and password"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(name=name, email=email, password=hashed_password.decode("utf-8"))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# --------- Login --------- #
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"error": "Invalid email or password"}), 401

    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return jsonify({"message": "Login successful", "token": token}), 200