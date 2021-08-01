from wtforms.form import FormMeta
from pcpc import app
from flask import render_template, request, flash, redirect, url_for, jsonify
import json, os
from pcpc.models import User, Team
from pcpc.forms import RegisterForm, LoginForm
from sqlalchemy import desc, or_
from pcpc import db, app, bcrypt, profile_pics, question_pics
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta
from datetime import date as ddate

@app.route("/")
def home():
    return render_template("main.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(current_user.user_type))

    form = LoginForm()
    user = User.query.filter(User.identifier==form.identifier.data).first()
    if form.validate_on_submit():
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("شماره دانشجویی یا رمز عبور اشتباه است", 'danger')
    data = {
        "hide_navbar": True
    }
    return render_template('login.html', form=form, **data)
@app.route("/register")
def register():
    return render_template("main.html")
