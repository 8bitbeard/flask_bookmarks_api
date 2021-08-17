from flask import Blueprint, json, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants import http_status_codes
import validators

from src.database.database import User, db


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register():
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']

    if len(password) < 6:
        return jsonify({
            'error': 'Password is too short!'
        }), http_status_codes.HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({
            'error': 'Username is too short!'
        }), http_status_codes.HTTP_400_BAD_REQUEST

    if not username.isalnum() or ' ' in username:
        return jsonify({
            'error': 'Username should be alphanumeric, anlso no spaces'
        }), http_status_codes.HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({
            'error': 'Email is not valid'
        }), http_status_codes.HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            'error': 'Email is taken'
        }), http_status_codes.HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
        'error': 'Username is taken'
    }), http_status_codes.HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created!',
        'user': {
            'username': username,
            'email': email
        }
    }), http_status_codes.HTTP_201_CREATED


    return "User created"

@auth.get('/me')
def me():
    return {"user": "me"}