from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required
from ..models import db, Settings
from ..routes.auth import admin_required
from ..translations import t

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route('/')
@admin_required
def index():
    lang = session.get('language', 'en')
    settings = Settings.get_all()
    return render_template('settings/index.html', settings=settings)


@settings_bp.route('/save', methods=['POST'])
@admin_required
def save():
    lang = session.get('language', 'en')
    
    mail_server = request.form.get('mail_server', '').strip()
    mail_port = request.form.get('mail_port', '587').strip()
    mail_use_tls = request.form.get('mail_use_tls') == 'on'
    mail_username = request.form.get('mail_username', '').strip()
    mail_password = request.form.get('mail_password', '').strip()
    mail_default_sender = request.form.get('mail_default_sender', '').strip()
    
    Settings.set('mail_server', mail_server)
    Settings.set('mail_port', mail_port)
    Settings.set('mail_use_tls', 'true' if mail_use_tls else 'false')
    Settings.set('mail_username', mail_username)
    Settings.set('mail_password', mail_password)
    Settings.set('mail_default_sender', mail_default_sender)
    
    flash(t('settings_saved', lang), 'success')
    return redirect(url_for('settings.index'))
