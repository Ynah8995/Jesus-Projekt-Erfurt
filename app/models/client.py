from .db import db
from datetime import datetime, date


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    birthday = db.Column(db.Date, nullable=False)
    privacy_signed = db.Column(db.Boolean, default=False)
    photo_permission = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def age(self):
        today = date.today()
        return today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )

    @property
    def birth_month(self):
        return self.birthday.month

    @property
    def birth_month_name(self):
        months_en = [
            '', 'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        return months_en[self.birthday.month]

    def __repr__(self):
        return f'<Client {self.first_name} {self.last_name}>'
