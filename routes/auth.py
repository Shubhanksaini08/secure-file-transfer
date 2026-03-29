from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from pymongo import MongoClient

auth = Blueprint('auth', __name__)
file_bp = Blueprint('file', __name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.secure_transfer

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    db.users.insert_one({
        "username": data['username'],
        "password": data['password']
    })
    return jsonify({"msg": "User Registered"})

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = db.users.find_one({"username": data['username']})

    if user and user['password'] == data['password']:
        token = create_access_token(identity=data['username'])
        return jsonify(access_token=token)

    return jsonify({"msg": "Invalid credentials"}), 401
@file_bp.route('/stats')
def stats():
    upload_count = db.files.count_documents({})
    return jsonify({"uploads": upload_count})