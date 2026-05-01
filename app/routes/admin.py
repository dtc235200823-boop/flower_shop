from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.product import Product, Category
from app.models.order import Order
from app.forms.product import CategoryForm, ProductForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def require_admin():
    """Require admin role"""
    if not current_user.is_admin():
        flash('Bạn không có quyền truy cập.', 'danger')
        return redirect(url_for('main.index'))

@admin_bp.route('/')
def dashboard():
    """Admin dashboard"""
    # Statistics
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Low stock products
    low_stock = Product.query.filter(Product.stock < 5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders,
                         low_stock=low_stock)

# Category management
@admin_bp.route('/categories')
def categories():
    """Manage categories"""
    page = request.args.get('page', 1, type=int)
    categories = Category.query.paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE']
    )
    return render_template('admin/categories/list.html', categories=categories)

@admin_bp.route('/categories/create', methods=['GET', 'POST'])
def create_category():
    """Create category"""
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data,
            is_active=form.is_active.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Danh mục đã được tạo.', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/categories/form.html', form=form)

@admin_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    """Edit category"""
    category = Category.query.get_or_404(category_id)
    form = CategoryForm()
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.is_active = form.is_active.data
        db.session.commit()
        flash('Danh mục đã được cập nhật.', 'success')
        return redirect(url_for('admin.categories'))
    
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
        form.is_active.data = category.is_active
    
    return render_template('admin/categories/form.html', form=form, category=category)

@admin_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    """Delete category"""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Danh mục đã được xóa.', 'success')
    return redirect(url_for('admin.categories'))

# User management
@admin_bp.route('/users')
def users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE']
    )
    return render_template('admin/users/list.html', users=users)

@admin_bp.route('/users/<int:user_id>/edit-role', methods=['POST'])
def edit_user_role(user_id):
    """Edit user role"""
    user = User.query.get_or_404(user_id)
    role = request.form.get('role')
    
    if role in ['customer', 'staff', 'admin']:
        user.role = role
        db.session.commit()
        flash(f'Vai trò của người dùng {user.username} đã được cập nhật.', 'success')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
def toggle_user_active(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'kích hoạt' if user.is_active else 'vô hiệu hóa'
    flash(f'Tài khoản {user.username} đã được {status}.', 'success')
    return redirect(url_for('admin.users'))

# Statistics & Reports
@admin_bp.route('/reports')
def reports():
    """Statistics and reports"""
    # Order statistics
    total_orders = Order.query.count()
    completed_orders = Order.query.filter_by(status='delivered').count()
    pending_orders = Order.query.filter_by(status='pending').count()
    
    # Revenue
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    # Top products
    from sqlalchemy import func
    top_products = db.session.query(
        Product.id,
        Product.name,
        func.sum(Order.items.quantity).label('total_sold')
    ).join(Order.items).group_by(Product.id).order_by('total_sold').limit(10).all()
    
    return render_template('admin/reports.html',
                         total_orders=total_orders,
                         completed_orders=completed_orders,
                         pending_orders=pending_orders,
                         total_revenue=total_revenue,
                         top_products=top_products)
