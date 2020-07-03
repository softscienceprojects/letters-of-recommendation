import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # DEBUG = False
    # TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or \
        'sqlite:///' + os.path.join(basedir, 'letters-development.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUD_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUD_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
    FLASK_ENV = os.environ.get('FLASK_ENV')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True
    DEBUG = True