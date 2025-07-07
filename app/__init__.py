import os
from flask import Flask, session
from .extensions import db, login_manager

def create_app():
    # Get absolute path to root/static
    basedir = os.path.abspath(os.path.dirname(__file__))
    static_dir = os.path.join(basedir, '..', 'static')

    app = Flask(__name__, static_folder=static_dir, static_url_path='/static')

    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gracedocs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @app.before_request
    def make_session_permanent():
        session.permanent = False

    from .models import User, PreVisitForm, Upload

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    return app
