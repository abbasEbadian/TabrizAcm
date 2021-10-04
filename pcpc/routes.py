from wtforms.form import FormMeta
from pcpc import app
from flask import render_template, request, flash, redirect, url_for, jsonify, abort
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
        "announcements": Announcement.query.all()
    }
    return render_template("home.html", **data)

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

@app.route("/rules")
def rules():
    return render_template("rules.html")


@app.route("/registeration")
def registeration2():
    return render_template("registeration.html")


@app.route('/admin/<menu_name>/edit/<param1>',  methods=["POST", "GET"])
@app.route('/admin/<menu_name>', methods=["POST", "GET"])
@app.route('/admin/')
@login_required
def admin(menu_name=None, param1=None):
    if not menu_name: return redirect('/admin/announcements')
    admin_template_path = os.path.join(app.instance_path.replace('instance', app.config['APP_NAME']), 'templates', 'admin')
    if not os.path.isfile(os.path.join(admin_template_path, menu_name+'.html')):
        abort(404)
    if not current_user.is_admin: 
        abort(403)
    data = {
        "teams": Team.query.all(),
        "contacts": ContactUs.query.all(),
        "teams": Team.query.all(),
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
            print(title, image , html)
            if not param1:
                a = Announcement(title=title, html=html)
                if image:
                    announcement_pics.save(image)
                    a.image = os.path.join(app.config.get("UPLOADED_ANNOUNCEMENTPICS_DEST") + image.filename)
                flash("با موفقیت ایجاد شد.", "info")
                db.session.add(a)
            else:
                ann = Announcement.query.filter_by(id=int(param1)).first()
                if ann:
                    ann.title = title
                    ann.html = html
                    print(image)
                    if image:
                        announcement_pics.save(image)
                        ann.image =os.path.join(app.config.get("UPLOADED_ANNOUNCEMENTPICS_DEST") + image.filename)
                    flash("با موفقیت تغییر یافت", "info")
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
        image = request.files and request.files['image'] or None
        if image and image.filename and image.filename != current_user.image.split("/")[-1]:
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





@app.route('/teams', methods=["POST", "GET"])
def get_teams():
    teams = [t.j for t in Team.query.all()]
    teams = tuple([{**r, "id": t+1} for t,r in enumerate(teams)])
    return jsonify(teams)
    # return {"data": teams}


@app.route('/team/delete/<code>', methods=["POST", "GET"])
@login_required
def delete_team(code):
    message = "success"
    t = Team.query.filter_by(code=code)
    if current_user.is_admin and t:
        t.delete()
        db.session.commit()
    else:
        message = "fail"

    return jsonify({"result": message})


@app.route('/team/name', methods=["POST"])
@login_required
def update_team_name():
    name = request.form.get("name")
    team_code = request.form.get("code")
    if team_code:
        t = Team.query.filter_by(code=team_code).first()
        print(t)
        if t:t.name = name
        db.session.commit() 

    else:
        t = Team(name=name, code=team_code)
        db.session.add(t)
    db.session.commit() 
    return jsonify({"result":"success"})

@app.route('/team/city', methods=["POST"])
@login_required
def update_team_city():
    city = request.form.get("city")
    team_code = request.form.get("code")
    if team_code:
        t = Team.query.filter_by(code=team_code).first()
        if t:t.city = city
        db.session.commit() 
    db.session.commit() 
    return jsonify({"result":"success"})
