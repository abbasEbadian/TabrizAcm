from wtforms.form import FormMeta
from pcpc import app
from flask import render_template, request, flash, redirect, url_for, jsonify
import json, os
from pcpc.models import User, Team
from pcpc.forms import RegisterForm, LoginForm, ProfileForm
from sqlalchemy import desc, or_
from pcpc import db, app, bcrypt, profile_pics, question_pics
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta
from datetime import date as ddate

@app.route("/")
def home():
    data = {
        "title":"PCPC - Tabriz",
        "navbar_theme": "white_theme"
    }
    return render_template("home.html", **data)

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
        return redirect(url_for('profile'))

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

@app.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    form = ProfileForm() 
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        flash('با موفقیت ذخیره شد', "info")
        image = request.files['image']
        if image.filename and image.filename != current_user.image.split("/")[-1]:
            for ext in ['.png', '.jpg', '.jpeg']:
                p = os.getcwd() + current_user.image + ext
                if os.path.isfile(p):
                    os.remove(p)
            profile_pics.save(image)
            current_user.image = f"uploads/profile_pics/{image.filename}"
        db.session.commit()
    data = {
        "form": form,
        "title": "PCPC - Profile",
        "navbar_theme": "white_theme"
    }
    return render_template('profile.html', **data)