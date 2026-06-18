"""
Database models for desktop app
Uses SQLAlchemy same as web version
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

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or self.username


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    address = Column(String(200), nullable=True)
    phone = Column(String(30), nullable=True)
    email = Column(String(120), nullable=True)
    birthday = Column(Date, nullable=False)
    privacy_signed = Column(Boolean, default=False)
    photo_permission = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )


class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    key = Column(String(50), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db(db_path):
    """Initialize database, return engine and session"""
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session()
