from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants import http_status_codes
import validators

from src.models import User
from src.database import db


class AuthService():

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
