import os

from flask import Flask

from flask_bcrypt import Bcrypt

from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.api.users import users_blueprint
    from app.api.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(users_blueprint)

    return app
