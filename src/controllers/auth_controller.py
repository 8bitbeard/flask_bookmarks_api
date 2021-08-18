from os import access
from src.constants.http_status_codes import HTTP_207_MULTI_STATUS
from flask import Blueprint, request, jsonify
import jwt
from werkzeug.security import check_password_hash

from src.models import User, user

from src.services import AuthService

from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from src.constants import http_status_codes


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register():

    data = request.json

    return AuthService.save_new_user(data)


@auth.post('/login')
def login():

    data = request.json

    return AuthService.login(data)


@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()

    return AuthService.get_user(user_id)


@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    user_id = get_jwt_identity()

    return AuthService.refresh_user_token(user_id)


@auth.get('/users')
def get_all():
    objects = User.query.all()

    users = []

    for user in objects:
        users.append({
            'username': user.username,
            'email': user.email
        })

    return jsonify({
        'users': users
    })