from datetime import datetime, time
from pcpc import db, login_manager
from flask_login import UserMixin
import jdatetime, random
from flask import url_for, jsonify
from functools import partial
DATE_FORMAT = "%Y/%m/%d"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    identifier = db.Column(db.String(10), nullable=False, unique=True)
    user_type = db.Column(db.String(30), default='member')
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    team = db.relationship('Team', backref=db.backref("members"))
    image = db.Column(db.String(100), default='img/default_user.png')
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_admin(self):
        return self.id == 1

    def __repr__(self):
        return f"{self.id or ''} : {self.name or ''} : {self.identifier or ''} "
    
def _gencode():
    return "Team-"+str(random.randint(1001,9999))

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, default=_gencode)
    name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    team_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    
    @property
    def unicode(self):
        return self.code
    @property
    def j(self):
        x = {
            "name": self.name,
            "code": self.unicode,
            "city": self.city,
            "members": len(User.query.join(Team).filter_by(unicode=self.unicode).all())
        }
        print(x)
        return x

    def __repr__(self):
        # return f"{self.id or ''} : {self.name or ''} : {self.code or ''}"
        return f"{self.id or ''}: {self.name or ''} : {self.code or ''}"

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
