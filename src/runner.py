import os

from src import create_app

from src.database import db


application = create_app(os.environ['FLASK_ENV'])
db.create_all()