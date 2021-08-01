from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField, BooleanField,IntegerField, TextAreaField
from wtforms import  SelectField, HiddenField, DateTimeField
from flask_wtf.file import FileField
from wtforms.fields.html5 import TelField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, length, EqualTo, ValidationError
from online_test.models import User, Course
from flask_login import current_user

length_message = "حداقل {} کاراکتر"
empty_message = "نمی تواند خالی باشد"
match_message = "رمز عبور های وارد شده یکسان نیستند"
class RegisterForm(FlaskForm):
    name = StringField('نام و نام خانوادگی', validators=[DataRequired(message=empty_message), length(min=5, max=100, message=length_message.format(5))])
    identifier = StringField('شماره دانشجویی',
        validators=[DataRequired(message=empty_message),length(min=9, max=100, message=length_message.format(9))],
        render_kw={"placeholder": "ده رقمی"})
    phone = TelField('شماره همراه',
        validators=[DataRequired(message=empty_message), length(min=11, max=11, message=length_message.format(11))],
        render_kw={"placeholder": "09..."})
    team = StringField('نام تیم', validators=[DataRequired(message=empty_message), length(min=5, max=20, message=length_message.format(5))])
    password = PasswordField('رمز عبور', validators=[DataRequired(message=empty_message)])
    confirm_password = PasswordField('تکرار رمز عبور', validators=[DataRequired(message=empty_message), EqualTo('password', message=match_message)])
    is_teacher = BooleanField('ثبت نام به عنوان استاد')
    submit = SubmitField('ثبت نام')

    def validate_identifier(self, identifier):
        user = User.query.filter_by(identifier=identifier.data).first()
        if user:
            raise ValidationError("این نام کاربری قبلا ثبت شده است.")
        
    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError("این شماره همراه قبلا ثبت شده است.")
        

class LoginForm(FlaskForm):
    identifier = StringField('شماره دانشجویی یا همراه', validators=[DataRequired(message=empty_message), length(min=5, max=20, message=length_message.format(5))])
    password = PasswordField('رمز عبور', validators=[DataRequired(message=empty_message)])
    remember = BooleanField('مرا به خاطر بسپار')
    submit = SubmitField('ورود به سایت')
