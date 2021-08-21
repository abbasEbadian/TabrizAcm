from datetime import datetime, time
from pcpc import db, login_manager
from flask_login import UserMixin
import jdatetime
from flask import url_for
DATE_FORMAT = "%Y/%m/%d"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    identifier = db.Column(db.String(10), nullable=False, unique=True)
    user_type = db.Column(db.String(30), default='member')
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    team = db.relationship('Team', backref=db.backref("members"))
    image = db.Column(db.String(100), default='img/default_user.png')
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')

    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_admin(self):
        return self.id == 1

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(identifier=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

    def __repr__(self):
        return str(self.id) + ":" + self.name + " " + self.identifier 
    

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(50))
    english_name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    english_city = db.Column(db.String(50))
    team_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return str(self.id) + ":" + self.name + " From " + self.city

class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    text = db.Column(db.String(200))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    html = db.Column(db.String(9999))
    image = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
