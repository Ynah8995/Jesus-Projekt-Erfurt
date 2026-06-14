from flask import Blueprint, render_template, request, session
from flask_login import login_required, current_user
from ..models import db, Client
from ..translations import t

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    lang = session.get('language', 'en')
    selected_month = request.args.get('month', type=int)

    total_clients = Client.query.count()

    if selected_month and 1 <= selected_month <= 12:
        clients = Client.query.filter(
            db.extract('month', Client.birthday) == selected_month
        ).order_by(
            db.extract('day', Client.birthday)
        ).all()
    else:
        clients = []
        selected_month = None

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
