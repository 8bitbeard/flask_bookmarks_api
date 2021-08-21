import os

from flask import Flask
from flask.json import jsonify

from flask_jwt_extended import JWTManager

from src.database import db, migrate

from src.controllers.auth_controller import auth
from src.controllers.bookmark_controller import bookmarks
from src.controllers.url_controller import url

from src.constants import http_status_codes

from src.config import config_by_name

basedir = os.path.abspath(os.path.dirname(__file__))
MIGRATION_DIR = os.path.join(basedir, 'database', 'migrations')


def create_app(config_name='development'):

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    app.app_context().push()
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db, directory=MIGRATION_DIR)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    app.register_blueprint(url)

    @app.errorhandler(http_status_codes.HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            'error': 'Not found'
        }), http_status_codes.HTTP_404_NOT_FOUND

    @app.errorhandler(http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({
            'error': 'Something went very very bad! We are working on it!!!'
        }), http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR

    return app
