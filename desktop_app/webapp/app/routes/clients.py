from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from ..models import db, Client
from ..routes.auth import admin_required
from ..translations import t
from datetime import datetime

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')


@clients_bp.route('/')
@login_required
def list_clients():
    lang = session.get('language', 'en')
    clients = Client.query.order_by(Client.last_name, Client.first_name).all()
    return render_template('clients/list.html', clients=clients)


@clients_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_client():
    lang = session.get('language', 'en')
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        birthday_str = request.form.get('birthday', '')
        privacy_signed = request.form.get('privacy_signed') == 'on'
        photo_permission = request.form.get('photo_permission') == 'on'

        if not first_name or not last_name or not birthday_str:
            flash(t('required_field', lang), 'error')
            return render_template('clients/form.html', client=None, mode='add')

        try:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        except ValueError:
            flash(t('required_field', lang), 'error')
            return render_template('clients/form.html', client=None, mode='add')

        client = Client(
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone,
            email=email,
            birthday=birthday,
            privacy_signed=privacy_signed,
            photo_permission=photo_permission
        )
        db.session.add(client)
        db.session.commit()
        flash(t('client_added', lang), 'success')
        return redirect(url_for('clients.list_clients'))

    return render_template('clients/form.html', client=None, mode='add')


@clients_bp.route('/edit/<int:client_id>', methods=['GET', 'POST'])
@login_required
def edit_client(client_id):
    lang = session.get('language', 'en')
    client = db.session.get(Client, client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('clients.list_clients'))

    if request.method == 'POST':
        client.first_name = request.form.get('first_name', '').strip()
        client.last_name = request.form.get('last_name', '').strip()
        client.address = request.form.get('address', '').strip()
        client.phone = request.form.get('phone', '').strip()
        client.email = request.form.get('email', '').strip()
        client.privacy_signed = request.form.get('privacy_signed') == 'on'
        client.photo_permission = request.form.get('photo_permission') == 'on'

        birthday_str = request.form.get('birthday', '')
        if birthday_str:
            try:
                client.birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            except ValueError:
                flash(t('required_field', lang), 'error')
                return render_template('clients/form.html', client=client, mode='edit')

        if not client.first_name or not client.last_name:
            flash(t('required_field', lang), 'error')
            return render_template('clients/form.html', client=client, mode='edit')

        db.session.commit()
        flash(t('client_updated', lang), 'success')
        return redirect(url_for('clients.list_clients'))

    return render_template('clients/form.html', client=client, mode='edit')


@clients_bp.route('/delete/<int:client_id>', methods=['GET', 'POST'])
@admin_required
def delete_client(client_id):
    lang = session.get('language', 'en')
    client = db.session.get(Client, client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('clients.list_clients'))

    if request.method == 'POST':
        admin_password = request.form.get('admin_password', '')
        if current_user.check_password(admin_password):
            db.session.delete(client)
            db.session.commit()
            flash(t('client_deleted', lang), 'success')
            return redirect(url_for('clients.list_clients'))
        else:
            flash(t('incorrect_password', lang), 'error')

    return render_template('clients/delete.html', client=client)
