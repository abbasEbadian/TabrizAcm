from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import configure_uploads, IMAGES, UploadSet
import os
from flask_assets import Environment, Bundle


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/db.sqlite"
app.config["SECRET_KEY"] = "17ab226de066a0f995895791b9e726fbb14042df6583763d1df5084dfc3b53e8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["APP_NAME"] = "pcpc"
app.config["UPLOADS_DEFAULT_DEST"] = app.config["APP_NAME"] + '/static'
app.config["UPLOADS_DEFAULT_URL"] = app.config["APP_NAME"] + '/static'
app.config["UPLOADED_PROFILEPICS_DEST"] = app.config["UPLOADS_DEFAULT_DEST"] + '/uploads/profile_pics'
app.config["UPLOADED_QUESTIONPICS_DEST"] = app.config["UPLOADS_DEFAULT_DEST"]+'/uploads/question_pics'
app.config["UPLOADED_ANNOUNCEMENTPICS_DEST"] = '/uploads/announcement_pics/'
app.config["UPLOADS_DEFAULT_URL"] = 'uploads/images'
app.config['UPLOAD_FOLDER'] = 'static/files/'
profile_pics = UploadSet('profilepics', IMAGES)
question_pics = UploadSet('questionpics', IMAGES)
announcement_pics = UploadSet('announcementpics', IMAGES)
configure_uploads(app, (profile_pics, question_pics, announcement_pics))
assets = Environment(app)
assets.url = app.static_url_path
assets.debug = True
scss_files = ['scss/index.scss','scss/responsive.scss', 'scss/profile.scss']
scss = Bundle( *scss_files , filters='pyscss', output='gen/all.css')
assets.register('scss_all', scss)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message  = "برای دسترسی به این صفحه ابتدا باید وارد شوید."
login_manager.login_message_category   = "info"

from pcpc.routes import *
from pcpc.models import *

if not User.query.first():
    db.session.add(User(name="admin",identifier="admin", password=bcrypt.generate_password_hash("admin")))
    db.session.commit()