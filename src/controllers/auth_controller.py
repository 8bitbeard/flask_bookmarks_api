from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from src.models import User

from src.services import AuthService

# from flask_jwt_extended import create_access_token, create_refresh_token
# from src.constants import http_status_codes


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register():

    data = request.json

    return AuthService.save_new_user(data)


@auth.post('/login')
def login():

    data = request.json

    return AuthService.login(data)

    # email = request.json['email']
    # password = request.json['password']

    # user = User.query.filter_by(email=email).first()

    # if user:
    #     is_pass_correct = check_password_hash(user.password, password)

    #     if is_pass_correct:
    #         access = create_access_token(identity=user.id)
    #         refresh = create_refresh_token(identity=user.id)

    #         return jsonify({
    #             'user': {
    #                 'email': user.email,
    #                 'username': user.username,
    #                 'access_token': access,
    #                 'refresh': refresh
    #             }
    #         })

    # return jsonify({
    #     'error': 'Wrong credentials'
    # }), http_status_codes.HTTP_401_UNAUTHORIZED



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