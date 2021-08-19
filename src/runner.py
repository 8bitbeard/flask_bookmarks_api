import os

from src import create_app


application = create_app(os.getenv['FLASK_ENV'])