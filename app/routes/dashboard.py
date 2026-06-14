from flask import Blueprint, render_template, request, session, jsonify
from flask_login import login_required, current_user
from ..models import db, Client
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
    
    data = request.get_json()
    subject_template = data.get('subject', t('greeting_subject', lang))
    message_template = data.get('message', t('greeting_message', lang))
    
    month_names = {
        1: t('january', lang), 2: t('february', lang), 3: t('march', lang),
        4: t('april', lang), 5: t('may', lang), 6: t('june', lang),
        7: t('july', lang), 8: t('august', lang), 9: t('september', lang),
        10: t('october', lang), 11: t('november', lang), 12: t('december', lang)
    }
    
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
            msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
            msg['To'] = client.email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                if current_app.config['MAIL_USE_TLS']:
                    server.starttls()
                if current_app.config['MAIL_USERNAME'] and current_app.config['MAIL_PASSWORD']:
                    server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
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
