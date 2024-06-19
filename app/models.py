from datetime import datetime
from flask_login import UserMixin
from app import db
from sqlalchemy.orm import mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.relationship('Note', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Note(db.Model):
    id = mapped_column(db.Integer, primary_key=True)
    title = mapped_column(db.String(128), nullable=False)
    content = mapped_column(db.Text, nullable=False)
    timestamp = mapped_column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
