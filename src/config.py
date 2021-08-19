import os

postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_bookmarks_dev.db')
    JWT_SECRET_TOKEN=os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_bookmarks_test.db')
    JWT_SECRET_TOKEN=os.environ.get('JWT_SECRET_KEY')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = {
    "development":DevelopmentConfig,
    "testing":TestingConfig,
    "production":ProductionConfig
}

key = Config.SECRET_KEY