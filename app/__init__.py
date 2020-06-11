import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db=SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    #migrate = Migrate(app, db)

    return app


from app.models import User, Post
from app.main import routes as main_routes
