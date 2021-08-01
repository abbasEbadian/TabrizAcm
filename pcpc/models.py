from datetime import datetime, time
from online_test import db, login_manager
from flask_login import UserMixin
import jdatetime
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
    team = db.relationship('Team', backref=db.backref("members", lazy="dynamic"))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return str(self.id) + ":" + self.name + " " + self.identifier 
    

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    team_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return str(self.id) + ":" + self.name + " From " + self.city