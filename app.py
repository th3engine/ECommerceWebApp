from flask import Flask, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from config import Config

from db import db, Users, Fragrances
from flask_migrate import Migrate

from resources import Home, Auth, Profile, admin, Checkout

migrate = Migrate()
bootstrap = Bootstrap5()

login_manager = LoginManager()

@login_manager.unauthorized_handler
def handles_needs_login():
    return redirect(url_for('Auth.login',next=request.endpoint))

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users,user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app,db)
    bootstrap.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)


    # Register Blueprints here
    app.register_blueprint(Home)
    app.register_blueprint(Auth)
    app.register_blueprint(Profile)
    app.register_blueprint(Checkout)

        


    return app

if __name__=='__main__':
    app = create_app()
    app.run(debug=True)