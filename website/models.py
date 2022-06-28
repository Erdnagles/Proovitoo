from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(150), unique=True)
    registryCode = db.Column(db.String, unique=True)
    registrationDate = db.Column(db.DateTime(timezone=True), default=func.now)
    capital = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_Name = db.Column(db.String(150))
    companies = db.relationship('Company')
