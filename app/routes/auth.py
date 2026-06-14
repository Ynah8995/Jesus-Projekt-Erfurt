from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from ..models import db, User
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
login_manager = None


def init_login_manager(app):
    global login_manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if not current_user.has_role('admin'):
            flash('Insufficient permissions.', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if not user.is_active:
                from ..translations import t
                flash(t('account_deactivated', session.get('language', 'en')), 'error')
                return render_template('auth/login.html')
            login_user(user)
            user.last_login = db.func.current_timestamp()
            db.session.commit()
            session['language'] = user.language or 'en'
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        from ..translations import t
        flash(t('login_error', session.get('language', 'en')), 'error')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-language/<lang>')
def change_language(lang):
    if lang in ['en', 'de']:
        session['language'] = lang
        if current_user.is_authenticated:
            current_user.language = lang
            db.session.commit()
    return redirect(request.referrer or url_for('dashboard.index'))
