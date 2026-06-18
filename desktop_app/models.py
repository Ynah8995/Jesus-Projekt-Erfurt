"""
Minimal models for the desktop launcher to create the first admin user.
The web app has its own models in webapp/app/models/
"""
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), nullable=False, default='staff')
    first_name = Column(String(80), nullable=True)
    last_name = Column(String(80), nullable=True)
    is_active = Column(Boolean, default=True)
    language = Column(String(2), default='en')
    profile_picture = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        return self.role == role
