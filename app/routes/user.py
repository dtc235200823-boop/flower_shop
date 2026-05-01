from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    from app.models.order import Order
    
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(
        Order.created_at.desc()
    ).all()
    
    return render_template('user/dashboard.html', orders=user_orders)

@user_bp.route('/profile')
@login_required
def profile():
    """User profile"""
    return render_template('user/profile.html')
