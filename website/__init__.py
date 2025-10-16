from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager #manages user sessions

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    # Configuration settings
    app.config['SECRET_KEY'] = 'cookie'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) 
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, AUser #, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #if a non logged in user tries to access a login required route they will be redirected to the login page
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(composite_id):
        try:
            user_type, user_id = composite_id.split('-')
            if user_type == "user":
                return User.query.get(int(user_id))
            elif user_type == "admin":
                return AUser.query.get(int(user_id))
        except Exception:
            return None

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')