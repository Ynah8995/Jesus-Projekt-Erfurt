import os
from flask import Flask, session, redirect, url_for
from flask_login import LoginManager
from .config import Config
from .models import db, User
from .routes.auth import auth_bp, init_login_manager
from .routes.dashboard import dashboard_bp
from .routes.clients import clients_bp
from .translations import t


def create_app(config_class=Config):
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config_class)

    db.init_app(app)
    init_login_manager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clients_bp)

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
        _create_default_admin(app)

    return app


def _create_default_admin(app):
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@jesus-projekt.de',
                first_name='Admin',
                last_name='User',
                role='admin',
                is_active=True,
                language='en'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("=" * 50)
            print("Default admin user created:")
            print("  Username: admin")
            print("  Password: admin123")
            print("  IMPORTANT: Change this password after first login!")
            print("=" * 50)
