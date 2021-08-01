from wtforms.form import FormMeta
from online_test import app
from flask import render_template, request, flash, redirect, url_for, jsonify
import json, os
from online_test.models import User, Team
from online_test.forms import RegisterForm, LoginForm
from sqlalchemy import desc, or_
from online_test import db, app, bcrypt, profile_pics, question_pics
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta
from datetime import date as ddate

# @app.route("/")
# def home():
#     return redirect(url_for(current_user.user_type))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden403(e):
    return render_template('403.html'), 403

@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(current_user.user_type))

    form = LoginForm()
    user = User.query.filter(or_(User.identifier==form.identifier.data,User.phone==form.identifier.data)).first()
    if form.validate_on_submit():
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for(user.user_type))
        else:
            flash("شماره دانشجویی یا رمز عبور اشتباه است", 'danger')

    return render_template('login.html', form=form, **data)
