import validators

from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from src.constants import http_status_codes

from src.models import User
from src.database import db


class AuthService:

    def save_new_user(data):
        if 'username' not in data:
            return jsonify({
                'error': 'Username empty or incorrect!'
            }), http_status_codes.HTTP_400_BAD_REQUEST

        if 'email' not in data:
            return jsonify({
                'error': 'Email is blank or incorrect!'
            })


        if 'password' not in data:
            return jsonify({
                'error': 'Password is blank or incorrect!'
            })

        username = data['username']
        email = data['email']
        password = data['password']


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

    def login(data):
        if 'email' not in data:
              return jsonify({
                'error': "Email can't be null!"
            })


        if 'password' not in data:
            return jsonify({
                'error': "Password can't be null!"
            })

        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if user:
            is_pass_correct = check_password_hash(user.password, password)

            if is_pass_correct:
                access = create_access_token(identity=user.id)
                refresh = create_refresh_token(identity=user.id)

                return jsonify({
                    'user': {
                        'email': user.email,
                        'username': user.username,
                        'access_token': access,
                        'refresh': refresh
                    }
                }), http_status_codes.HTTP_200_OK

        return jsonify({
            'error': 'Wrong credentials'
        }), http_status_codes.HTTP_401_UNAUTHORIZED

    def get_user(user_id):
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({
                'error': 'User not found!'
            }), http_status_codes.HTTP_404_NOT_FOUND

        return jsonify({
            'username': user.username,
            'email': user.email
        }), http_status_codes.HTTP_200_OK

    def refresh_user_token(user_id):
        access = create_access_token(identity=user_id)

        return jsonify({
            'access_token': access
        }), http_status_codes.HTTP_200_OK