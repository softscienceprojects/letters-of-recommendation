import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from app.config import *
from app.filters import *


basedir = os.path.abspath(os.path.dirname(__file__))
# BASE_CLOUDINARY_URL = f"https://res.cloudinary.com/{os.environ.get('CLOUDINARY_CLOUD_NAME')}/image/upload" 

db=SQLAlchemy()
migrate = Migrate(compare_type=True)
moment = Moment()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db) # remember it needs both app and db
    login.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    if app.config.get('ENV')=='production':
        logging.basicConfig(filename='logs/production.log', format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    
    # if not os.path.exists('logs'):
    #     os.mkdir('logs')
    # file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    # file_handler.setFormatter(logging.Formatter(
    #     '%(asctime)s %(levelname)s: %(message)s '
    #     '[in %(pathname)s:%(lineno)d]'))
    # file_handler.setLevel(logging.INFO)
    # app.logger.addHandler(file_handler)
    # app.logger.setLevel(logging.INFO)
    # app.logger.info('Letters of Recommendation starting up')


    app.jinja_env.filters['blogpost'] = display_blog_post
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.filters['daydateformat'] = daydateformat
    app.jinja_env.filters['poststatus'] = poststatus
    app.jinja_env.filters['test_erin'] = test_erin
    app.jinja_env.filters['image_url'] = get_self_image_for_select_buttons
    app.jinja_env.filters['autoversion'] = autoversion

    return app


from app.models import *