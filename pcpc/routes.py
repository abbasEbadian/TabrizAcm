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
    return render_template("main.html", title="PCPC - Tabriz")

@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    user = User.query.filter(User.identifier==form.identifier.data).first()
    if form.validate_on_submit():
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("شماره دانشجویی یا رمز عبور اشتباه است", 'danger')
    data = {
        "hide_navbar": True,
        "form": form,
        "title": "PCPC - Login"
    }
    return render_template('login.html', **data)
@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = {
            "name": form.name.data,
            "identifier": form.identifier.data,
            "password": hash_pwd,
            "email": form.email.data,
        }
        user = User(**new_user)
        db.session.add(user)
        db.session.commit()
        flash("حساب کاربری با موفقیت ایجاد شد.", 'success')
        return redirect(url_for('login'))

    data = {
        "hide_navbar": True,
        "form": form,
        "title": "PCPC - Register"
    }
    return render_template('register.html', **data)
