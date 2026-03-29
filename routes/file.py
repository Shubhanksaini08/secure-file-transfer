from flask_socketio import emit
from utils.hash import generate_hash
from utils.logger import log_event
from utils.encryption import encrypt_file, decrypt_file
from flask_socketio import SocketIO
from app import socketio
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

file_bp = Blueprint('file', __name__)

@file_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    user = get_jwt_identity()
    file = request.files['file']
    data = file.read()

    encrypted = encrypt_file(data)
    file_hash = generate_hash(data)

    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(encrypted)

    log_event(user, "UPLOAD", file.filename)

    # 🔴 REAL-TIME EVENT
    socketio.emit('activity', {
        "user": user,
        "action": "UPLOAD",
        "file": file.filename,
        "hash": file_hash
    })

    return jsonify({"msg": "File uploaded securely", "hash": file_hash})

@file_bp.route('/download/<filename>', methods=['GET'])
@jwt_required()
def download(filename):
    with open(f"uploads/{filename}", "rb") as f:
        encrypted = f.read()

    decrypted = decrypt_file(encrypted)

    return decrypted

import os
from flask import jsonify

@file_bp.route('/files', methods=['GET'])
@jwt_required()
def list_files():
    files = os.listdir("uploads")
    return jsonify({"files": files})


    upload_count = 0

@file_bp.route('/upload', methods=['POST'])
def upload():
    global upload_count
    upload_count += 1