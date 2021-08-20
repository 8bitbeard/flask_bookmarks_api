from flask import Flask
from flask.json import jsonify
from flask_migrate import Migrate


from flask_jwt_extended import JWTManager

from src.database import db

from src.controllers.auth_controller import auth
from src.controllers.bookmark_controller import bookmarks
from src.controllers.url_controller import url

from src.constants import http_status_codes

from src.config import config_by_name





# def create_app(test_config=None):

#     app = Flask(__name__, instance_relative_config=True)

#     if test_config is None:
#         app.config.from_mapping(
#             SECRET_KEY=os.environ.get("SECRET_KEY"),
#             SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
#             SQLALCHEMY_TRACK_MODIFICATIONS=False,
#             JWT_SECRET_TOKEN=os.environ.get('JWT_SECRET_KEY')
#         )
#     else:
#         app.config.from_mapping(test_config)

def create_app(config_name='development'):

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    migrate = Migrate(app, db)
    app.app_context().push()
    db.app=app
    db.init_app(app)

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
