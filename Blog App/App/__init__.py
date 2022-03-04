from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'
UPLOAD_FOLDER = 'App/static/img/'
folder = ''
app = None


def create_app():

    global folder
    global app

    #Initialize the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'This is my key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    folder = app.config['UPLOAD_FOLDER']

    #Configure the blueprints

    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(views, url_prefix = '/')

    #Setup the database
    db.init_app(app)
    create_database(app)

    #Configure the login manager

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):

        return User.query.get(int(id))

    return app




#Create the database with all the tables
def create_database(app):
    if(path.exists(f'App/{DB_NAME}')):
        db.create_all(app = app)