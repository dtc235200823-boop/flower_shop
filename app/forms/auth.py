from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models.user import User

class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Tên đăng nhập', validators=[
        DataRequired(), 
        Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    password = PasswordField('Mật khẩu', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Xác nhận mật khẩu', validators=[
        DataRequired(),
        EqualTo('password', message='Mật khẩu không trùng khớp')
    ])
    submit = SubmitField('Đăng ký')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Tên đăng nhập đã tồn tại')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email đã được đăng ký')

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember = BooleanField('Ghi nhớ tôi')
    submit = SubmitField('Đăng nhập')

class UpdateProfileForm(FlaskForm):
    """Update user profile form"""
    full_name = StringField('Họ và tên')
    phone = StringField('Số điện thoại')
    address = StringField('Địa chỉ')
    city = StringField('Thành phố')
    postal_code = StringField('Mã bưu điện')
    submit = SubmitField('Cập nhật')
