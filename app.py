from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
import bcrypt
import jwt
from functools import wraps
from datetime import datetime, timedelta

# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1299@localhost:5432/Secure_auth_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT settings
JWT_SECRET = "supersecretkey"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_HOURS = 1

# Initialize DB
db = SQLAlchemy(app)

# ------------------------
# User model
# ------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# ------------------------
# JWT decorator for protected routes
# ------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(payload, *args, **kwargs)
    return decorated

# ------------------------
# Registration Route
# ------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Please provide name, email, and password"}), 400

    # Check if user exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(name=name, email=email, password=hashed_password.decode("utf-8"))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# ------------------------
# Login Route
# ------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Please provide email and password"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXP_DELTA_HOURS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return jsonify({"message": "Login successful", "token": token}), 200

# ------------------------
# Protected Dashboard Route
# ------------------------
@app.route("/dashboard", methods=["GET"])
@token_required
def dashboard(payload):
    user_id = payload["user_id"]
    user = User.query.get(user_id)
    return jsonify({"message": f"Welcome {user.name}! This is your dashboard."})

# ------------------------
# Test home route
# ------------------------
@app.route("/")
def home():
    return "Secure Auth System Running 🚀"

# ------------------------
# Run with Waitress
# ------------------------
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=9090)