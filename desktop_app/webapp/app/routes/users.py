from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_required, current_user
from ..models import db, User
from ..routes.auth import admin_required
from ..translations import t
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
import uuid

users_bp = Blueprint('users', __name__, url_prefix='/users')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@users_bp.route('/')
@admin_required
def list_users():
    lang = session.get('language', 'en')
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('users/list.html', users=users)


@users_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    lang = session.get('language', 'en')
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        role = request.form.get('role', 'staff')
        
        if not username or not email or not password:
            flash(t('required_field', lang), 'error')
            return render_template('users/form.html', user=None, mode='add')
        
        if User.query.filter_by(username=username).first():
            flash(t('username_exists', lang), 'error')
            return render_template('users/form.html', user=None, mode='add')
        
        if User.query.filter_by(email=email).first():
            flash(t('email_exists', lang), 'error')
            return render_template('users/form.html', user=None, mode='add')
        
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=True,
            language='en'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash(t('user_added', lang), 'success')
        return redirect(url_for('users.list_users'))
    
    return render_template('users/form.html', user=None, mode='add')


@users_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    lang = session.get('language', 'en')
    user = db.session.get(User, user_id)
    
    if not user:
        flash(t('user_not_found', lang), 'error')
        return redirect(url_for('users.list_users'))
    
    if not current_user.has_role('admin') and current_user.id != user_id:
        flash(t('insufficient_permissions', lang), 'error')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        if not username or not email:
            flash(t('required_field', lang), 'error')
            return render_template('users/form.html', user=user, mode='edit')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user_id:
            flash(t('username_exists', lang), 'error')
            return render_template('users/form.html', user=user, mode='edit')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != user_id:
            flash(t('email_exists', lang), 'error')
            return render_template('users/form.html', user=user, mode='edit')
        
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        
        if current_user.has_role('admin'):
            user.role = request.form.get('role', user.role)
            user.is_active = request.form.get('is_active') == 'on'
        
        new_password = request.form.get('new_password', '').strip()
        if new_password:
            user.set_password(new_password)
        
        profile_picture = request.files.get('profile_picture')
        if profile_picture and profile_picture.filename:
            if allowed_file(profile_picture.filename):
                ext = profile_picture.filename.rsplit('.', 1)[1].lower()
                filename = f"user_{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
                upload_dir = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_dir, exist_ok=True)
                profile_picture.save(os.path.join(upload_dir, filename))
                
                if user.profile_picture:
                    old_file = os.path.join(upload_dir, user.profile_picture)
                    if os.path.exists(old_file):
                        os.remove(old_file)
                
                user.profile_picture = filename
        
        db.session.commit()
        flash(t('user_updated', lang), 'success')
        
        if current_user.id == user_id:
            return redirect(url_for('users.edit_user', user_id=user_id))
        return redirect(url_for('users.list_users'))
    
    return render_template('users/form.html', user=user, mode='edit')


@users_bp.route('/reset-password/<int:user_id>', methods=['POST'])
@admin_required
def reset_password(user_id):
    lang = session.get('language', 'en')
    user = db.session.get(User, user_id)
    
    if not user:
        flash(t('user_not_found', lang), 'error')
        return redirect(url_for('users.list_users'))
    
    new_password = request.form.get('new_password', '').strip()
    if not new_password:
        flash(t('required_field', lang), 'error')
        return redirect(url_for('users.edit_user', user_id=user_id))
    
    user.set_password(new_password)
    db.session.commit()
    
    flash(t('password_reset', lang) + f" {user.username}", 'success')
    return redirect(url_for('users.edit_user', user_id=user_id))


@users_bp.route('/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    lang = session.get('language', 'en')
    user = db.session.get(User, user_id)
    
    if not user:
        flash(t('user_not_found', lang), 'error')
        return redirect(url_for('users.list_users'))
    
    if user.id == current_user.id:
        flash(t('cannot_delete_self', lang), 'error')
        return redirect(url_for('users.list_users'))
    
    if user.profile_picture:
        upload_dir = current_app.config['UPLOAD_FOLDER']
        old_file = os.path.join(upload_dir, user.profile_picture)
        if os.path.exists(old_file):
            os.remove(old_file)
    
    db.session.delete(user)
    db.session.commit()
    
    flash(t('user_deleted', lang), 'success')
    return redirect(url_for('users.list_users'))
