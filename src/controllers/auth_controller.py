from flask import Blueprint, request, jsonify

from src.models import User

from src.services import AuthService


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register():

    data = request.json

    return AuthService.save_new_user(data)


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