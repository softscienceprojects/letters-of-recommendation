from dotenv import load_dotenv
import os
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

class Config(object):
    # DEBUG = False
    # TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-really-needs-to-be-changed'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'my_previous_two'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or \
        'sqlite:///' + os.path.join(basedir, 'letters-development.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUD_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUD_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
    """
    If using STARTTLS with MAIL_USE_TLS = True, then use MAIL_PORT = 587.
    If using SSL/TLS directly with MAIL_USE_SSL = True, then use MAIL_PORT = 465.
    """
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')


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