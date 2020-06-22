import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from config import Config
from app.filters import display_blog_post, datetimeformat


basedir = os.path.abspath(os.path.dirname(__file__))


db=SQLAlchemy()
migrate = Migrate()
moment = Moment()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db) # remember it needs both app and db
    login.init_app(app)
    moment.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    app.jinja_env.filters['blogpost'] = display_blog_post
    app.jinja_env.filters['datetimeformat'] = datetimeformat

    return app


from app.models import User, Post
