from flask import Blueprint, render_template, request, session, jsonify
from flask_login import login_required, current_user
from ..models import db, Client, Settings
from ..translations import t
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    lang = session.get('language', 'en')
    selected_month = request.args.get('month', type=int)

    if selected_month and 1 <= selected_month <= 12:
        session['selected_month'] = selected_month
    elif 'selected_month' in session:
        selected_month = session['selected_month']
    else:
        selected_month = None

    total_clients = Client.query.count()

    if selected_month and 1 <= selected_month <= 12:
        clients = Client.query.filter(
            db.extract('month', Client.birthday) == selected_month
        ).order_by(
            db.extract('day', Client.birthday)
        ).all()
    else:
        clients = []

    months = [
        (1, t('january', lang)),
        (2, t('february', lang)),
        (3, t('march', lang)),
        (4, t('april', lang)),
        (5, t('may', lang)),
        (6, t('june', lang)),
        (7, t('july', lang)),
        (8, t('august', lang)),
        (9, t('september', lang)),
        (10, t('october', lang)),
        (11, t('november', lang)),
        (12, t('december', lang)),
    ]

    return render_template('dashboard/index.html',
                           total_clients=total_clients,
                           clients=clients,
                           months=months,
                           selected_month=selected_month)


@dashboard_bp.route('/send-greetings', methods=['POST'])
@login_required
def send_greetings():
    lang = session.get('language', 'en')
    selected_month = session.get('selected_month')
    
    if not selected_month:
        return jsonify({'success': False, 'message': t('select_month', lang)}), 400
    
    clients = Client.query.filter(
        db.extract('month', Client.birthday) == selected_month,
        Client.email.isnot(None),
        Client.email != ''
    ).all()
    
    if not clients:
        return jsonify({'success': False, 'message': t('no_email_clients', lang)}), 400
    
    mail_username = Settings.get('mail_username')
    mail_password = Settings.get('mail_password')
    
    if not mail_username or not mail_password:
        return jsonify({'success': False, 'message': t('mail_not_configured', lang)}), 400
    
    mail_server = Settings.get('mail_server', 'smtp.gmail.com')
    mail_port = int(Settings.get('mail_port', '587'))
    mail_use_tls = Settings.get('mail_use_tls', 'true') == 'true'
    mail_default_sender = Settings.get('mail_default_sender', mail_username)
    
    data = request.get_json()
    subject_template = data.get('subject', t('greeting_subject', lang))
    message_template = data.get('message', t('greeting_message', lang))
    
    sent_count = 0
    errors = []
    
    for client in clients:
        try:
            name = f"{client.first_name} {client.last_name}"
            subject = subject_template.replace('{name}', name)
            subject = subject.replace('{first_name}', client.first_name)
            subject = subject.replace('{last_name}', client.last_name)
            
            message = message_template.replace('{name}', name)
            message = message.replace('{first_name}', client.first_name)
            message = message.replace('{last_name}', client.last_name)
            
            msg = MIMEMultipart()
            msg['From'] = mail_default_sender
            msg['To'] = client.email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            with smtplib.SMTP(mail_server, mail_port) as server:
                if mail_use_tls:
                    server.starttls()
                server.login(mail_username, mail_password)
                server.send_message(msg)
            
            sent_count += 1
        except Exception as e:
            errors.append(f"{client.first_name} {client.last_name}: {str(e)}")
    
    if sent_count > 0:
        return jsonify({
            'success': True, 
            'message': f"{sent_count} {t('greetings_sent', lang)}",
            'errors': errors
        })
    else:
        return jsonify({
            'success': False, 
            'message': t('greeting_error', lang),
            'errors': errors
        }), 500
