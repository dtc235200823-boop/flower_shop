from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.forms.auth import RegistrationForm, LoginForm, UpdateProfileForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.username.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Tài khoản của bạn đã bị vô hiệu hóa.', 'danger')
            else:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Bạn đã đăng xuất.', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile"""
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.postal_code = form.postal_code.data
        
        db.session.commit()
        flash('Hồ sơ đã được cập nhật.', 'success')
        return redirect(url_for('auth.profile'))
    
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.phone.data = current_user.phone
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.postal_code.data = current_user.postal_code
    
    return render_template('auth/profile.html', form=form)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password"""
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(old_password):
            flash('Mật khẩu cũ không đúng.', 'danger')
        elif new_password != confirm_password:
            flash('Mật khẩu mới không trùng khớp.', 'danger')
        elif len(new_password) < 6:
            flash('Mật khẩu phải có ít nhất 6 ký tự.', 'danger')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Mật khẩu đã được thay đổi.', 'success')
            return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html')
