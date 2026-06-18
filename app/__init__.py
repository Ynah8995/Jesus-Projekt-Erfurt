import os
from flask import Flask, session, redirect, url_for
from flask_login import LoginManager
from .config import Config
from .models import db, User
from .routes.auth import auth_bp, init_login_manager
from .routes.dashboard import dashboard_bp
from .routes.clients import clients_bp
from .routes.settings import settings_bp
from .routes.users import users_bp
from .translations import t


def create_app(config_class=Config):
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config_class)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    init_login_manager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(users_bp)

    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))

    @app.context_processor
    def inject_translations():
        lang = session.get('language', 'en')
        return {'t': t, 'lang': lang}

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        return response

    with app.app_context():
        db.create_all()

    return app
