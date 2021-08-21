from wtforms.form import FormMeta
from pcpc import app
from flask import render_template, request, flash, redirect, url_for, jsonify
import json, os
from pcpc.models import User, Team, ContactUs, Announcement
from pcpc.forms import RegisterForm, LoginForm, ProfileForm, ContactForm, AnnounceForm
from sqlalchemy import desc, or_
from pcpc import db, app, bcrypt, profile_pics, question_pics, announcement_pics
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta
from datetime import date as ddate

@app.route('/api')
def api():
    return {
        "count": "1"
    }
@app.route("/")
def home():
    data = {
        "title":"PCPC - Tabriz",
        "navbar_logo_color": "white",
        "navbar_text_color": "white",
    }
    return render_template("home.html", **data)

@app.route('/admin/<menu_name>/edit/<param1>')
@app.route('/admin/<menu_name>', methods=["POST", "GET"])
@app.route('/admin/')
@login_required
def admin(menu_name=None, param1=None):
    if not menu_name: return redirect('/admin/announcements')
    admin_template_path = os.path.join(app.instance_path.replace('instance', app.config['APP_NAME']), 'templates', 'admin')
    if not os.path.isfile(os.path.join(admin_template_path, menu_name+'.html')):
        return page_not_found(404)
    if not current_user.is_admin: 
        return forbidden403(403)
    data = {
        "teams": Team.query.all(),
        "contacts": ContactUs.query.all(),
        "title": "ادمین اطلاعیه ها",
        "hide_navbar": True
    }    
    if menu_name == 'announcements':
        form = AnnounceForm()
        data["form"] = form
        if form.validate_on_submit():
            title = form.title.data
            image = form.image.data
            html = form.html.data
            announcement_pics.save(image)
            if not param1:
                a = Announcement(title=title, html=html)
                a.image = "uploads/announcement_pics/" + image.filename
                flash("با موفقیت ایجاد شد.", "info")
                db.session.add(a)
            else:
                ann = Announcement.query.get(int(param1))
                if ann:
                    ann.title = title
                    ann.html = html
                    ann.image = image
                    
            db.session.commit()
        if param1:
            ann = Announcement.query.get(int(param1))
            data["edit_ann"] = ann

           
    data["announcements"] =  Announcement.query.all()
    return render_template(f"/admin/{menu_name}.html", **data)


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
        "navbar_theme": "white_theme",
        "navbar_logo_color": "white",
        "navbar_text_color": "white",
    }
    return render_template('profile.html', **data)

@app.route('/contact-us', methods=["POST", "GET"])
@login_required
def contact_us():
    form = ContactForm() 
    if form.validate_on_submit():
        a = dict(
            name = form.name.data,
            email = form.email.data,
            text = form.text.data,
        )
        
        db.session.add(ContactUs(**a))
        db.session.commit()
        flash('با موفقیت ارسال شد', "info")
    data = {
        "form": form,
        "title": "PCPC - Contect us",
        "navbar_theme": "white_theme",
        "navbar_logo_color": "colored",
        "navbar_text_color": "white",
    }
    return render_template('contact-us.html', **data)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect( url_for("login") )


@app.route('/delete/announcement/<int:id>', methods=["GET", "POST"])
@login_required
def delete_announcement(id):
    ann = Announcement.query.get(int(id))
    if ann:
        db.session.delete(ann)
        db.session.commit()
        flash('با موفقیت حذف شد.', 'success')
    else:
        flash('خطا !', "danger")
    admin('announcements')