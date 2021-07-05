from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
# from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config['SECRET_KEY'] = 'Viusatq5237@#$hjbfe898&HBWFB1iudsfb'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .uploader.views import uploader
    # from .auth import auth

    app.register_blueprint(uploader, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')

    from .uploader.models import Progress


    create_database(app)

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('Created Database!')