from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User

class UserManagementForm(FlaskForm):
    """Form for creating and editing users (admin only)"""
    username = StringField('Tên đăng nhập', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    full_name = StringField('Họ tên', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    phone = StringField('Số điện thoại', validators=[Length(max=20)])
    password = PasswordField('Mật khẩu', validators=[
        Length(min=6, message='Mật khẩu phải có ít nhất 6 ký tự')
    ])
    password_confirm = PasswordField('Xác nhận mật khẩu', validators=[
        EqualTo('password', message='Mật khẩu không khớp')
    ])
    role = SelectField('Vai trò', choices=[
        ('customer', 'Khách hàng'),
        ('staff', 'Nhân viên'),
        ('admin', 'Quản trị viên')
    ], validators=[DataRequired()])
    is_active = BooleanField('Kích hoạt tài khoản')
    submit = SubmitField('Lưu')
    
    def validate_username(self, field):
        """Check if username already exists"""
        user = User.query.filter_by(username=field.data).first()
        if user and (not hasattr(self, 'original_user') or user.id != getattr(self.original_user, 'id', None)):
            raise ValidationError('Tên đăng nhập đã tồn tại.')
    
    def validate_email(self, field):
        """Check if email already exists"""
        user = User.query.filter_by(email=field.data).first()
        if user and (not hasattr(self, 'original_user') or user.id != getattr(self.original_user, 'id', None)):
            raise ValidationError('Email đã được sử dụng.')


class UserEditForm(FlaskForm):
    """Form for editing user details (without password change)"""
    username = StringField('Tên đăng nhập', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    full_name = StringField('Họ tên', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    phone = StringField('Số điện thoại', validators=[Length(max=20)])
    role = SelectField('Vai trò', choices=[
        ('customer', 'Khách hàng'),
        ('staff', 'Nhân viên'),
        ('admin', 'Quản trị viên')
    ], validators=[DataRequired()])
    is_active = BooleanField('Kích hoạt tài khoản')
    submit = SubmitField('Cập nhật')


class UserPasswordForm(FlaskForm):
    """Form for changing user password (admin)"""
    password = PasswordField('Mật khẩu mới', validators=[
        DataRequired(),
        Length(min=6, message='Mật khẩu phải có ít nhất 6 ký tự')
    ])
    password_confirm = PasswordField('Xác nhận mật khẩu', validators=[
        DataRequired(),
        EqualTo('password', message='Mật khẩu không khớp')
    ])
    submit = SubmitField('Đặt lại mật khẩu')
