from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db
from app.models.product import Product, Category
from app.models.review import Review
from app.forms.product import ProductForm, ReviewForm, CategoryForm
from app.models.user import User

product_bp = Blueprint('product', __name__)

def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_picture(form_picture):
    """Save picture to static/uploads"""
    if form_picture and allowed_file(form_picture.filename):
        filename = secure_filename(form_picture.filename)
        import uuid
        filename = str(uuid.uuid4()) + '_' + filename
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form_picture.save(filepath)
        return filename
    return None

@product_bp.route('/')
def list():
    """List all products"""
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(is_active=True).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE']
    )
    categories = Category.query.filter_by(is_active=True).all()
    return render_template('products/list.html', products=products, categories=categories)

@product_bp.route('/<int:product_id>')
def detail(product_id):
    """Product detail page"""
    product = Product.query.get_or_404(product_id)
    product.view_count += 1
    db.session.commit()
    
    form = ReviewForm()
    reviews = Review.query.filter_by(product_id=product_id, is_approved=True).all()
    related_products = Product.query.filter_by(
        category_id=product.category_id,
        is_active=True
    ).filter(Product.id != product_id).limit(4).all()
    
    return render_template('products/detail.html',
                         product=product,
                         form=form,
                         reviews=reviews,
                         related_products=related_products)

@product_bp.route('/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    """Add product review"""
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()
    
    if form.validate_on_submit():
        # Check if user already reviewed this product
        existing_review = Review.query.filter_by(
            product_id=product_id,
            user_id=current_user.id
        ).first()
        
        if existing_review:
            flash('Bạn đã đánh giá sản phẩm này rồi.', 'warning')
        else:
            review = Review(
                product_id=product_id,
                user_id=current_user.id,
                rating=form.rating.data,
                title=form.title.data,
                comment=form.comment.data
            )
            db.session.add(review)
            db.session.commit()
            flash('Đánh giá của bạn đã được gửi!', 'success')
    
    return redirect(url_for('product.detail', product_id=product_id))

# Admin routes
@product_bp.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    """Manage products (admin only)"""
    if not current_user.is_admin():
        flash('Bạn không có quyền truy cập.', 'danger')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    category_filter = request.args.get('category', 0, type=int)
    
    query = Product.query
    
    # Apply search filter
    if search_query:
        query = query.filter(
            (Product.name.ilike(f'%{search_query}%')) |
            (Product.description.ilike(f'%{search_query}%'))
        )
    
    # Apply category filter
    if category_filter:
        query = query.filter_by(category_id=category_filter)
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE']
    )
    
    categories = Category.query.all()
    
    return render_template('admin/products/list.html', 
                         products=products, 
                         categories=categories,
                         search_query=search_query,
                         current_category=category_filter)

@product_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new product"""
    if not current_user.is_admin():
        flash('Bạn không có quyền truy cập.', 'danger')
        return redirect(url_for('main.index'))
    
    form = ProductForm()
    categories = Category.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        try:
            image_file = save_picture(form.image.data)
            
            product = Product(
                name=form.name.data,
                description=form.description.data,
                category_id=form.category_id.data,
                price=form.price.data,
                stock=form.stock.data,
                color=form.color.data,
                quantity_per_item=form.quantity_per_item.data,
                origin=form.origin.data,
                image=image_file,
                is_featured=form.is_featured.data,
                is_active=form.is_active.data
            )
            
            db.session.add(product)
            db.session.commit()
            
            flash(f'✓ Sản phẩm "{form.name.data}" đã được tạo thành công!', 'success')
            return redirect(url_for('product.manage'))
        except Exception as e:
            db.session.rollback()
            flash(f'✗ Lỗi: {str(e)}', 'danger')
    
    return render_template('admin/products/form.html', form=form)

@product_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(product_id):
    """Edit product"""
    product = Product.query.get_or_404(product_id)
    
    if not current_user.is_admin():
        flash('Bạn không có quyền truy cập.', 'danger')
        return redirect(url_for('main.index'))
    
    form = ProductForm()
    categories = Category.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        try:
            product.name = form.name.data
            product.description = form.description.data
            product.category_id = form.category_id.data
            product.price = form.price.data
            product.stock = form.stock.data
            product.color = form.color.data
            product.quantity_per_item = form.quantity_per_item.data
            product.origin = form.origin.data
            product.is_featured = form.is_featured.data
            product.is_active = form.is_active.data
            
            if form.image.data:
                image_file = save_picture(form.image.data)
                if image_file:
                    product.image = image_file
            
            db.session.commit()
            flash(f'✓ Sản phẩm "{product.name}" đã được cập nhật thành công!', 'success')
            return redirect(url_for('product.manage'))
        except Exception as e:
            db.session.rollback()
            flash(f'✗ Lỗi: {str(e)}', 'danger')
    
    elif request.method == 'GET':
        form.name.data = product.name
        form.description.data = product.description
        form.category_id.data = product.category_id
        form.price.data = product.price
        form.stock.data = product.stock
        form.color.data = product.color
        form.quantity_per_item.data = product.quantity_per_item
        form.origin.data = product.origin
        form.is_featured.data = product.is_featured
        form.is_active.data = product.is_active
    
    return render_template('admin/products/form.html', form=form, product=product)

@product_bp.route('/<int:product_id>/toggle-active', methods=['POST'])
@login_required
def toggle_active(product_id):
    """Toggle product active status"""
    product = Product.query.get_or_404(product_id)
    
    if not current_user.is_admin():
        return {'error': 'Unauthorized'}, 403
    
    product.is_active = not product.is_active
    db.session.commit()
    
    return {
        'success': True,
        'is_active': product.is_active,
        'message': f'Sản phẩm {"đã kích hoạt" if product.is_active else "đã tắt"}'
    }

@product_bp.route('/<int:product_id>/toggle-featured', methods=['POST'])
@login_required
def toggle_featured(product_id):
    """Toggle product featured status"""
    product = Product.query.get_or_404(product_id)
    
    if not current_user.is_admin():
        return {'error': 'Unauthorized'}, 403
    
    product.is_featured = not product.is_featured
    db.session.commit()
    
    return {
        'success': True,
        'is_featured': product.is_featured,
        'message': f'Sản phẩm {"là nổi bật" if product.is_featured else "không nổi bật"}'
    }
    """Delete product"""
    product = Product.query.get_or_404(product_id)
    
    if not current_user.is_admin():
        flash('Bạn không có quyền truy cập.', 'danger')
        return redirect(url_for('main.index'))
    
    product_name = product.name
    
    # Delete associated reviews
    Review.query.filter_by(product_id=product_id).delete()
    
    # Delete product
    db.session.delete(product)
    db.session.commit()
    
    flash(f'✓ Sản phẩm "{product_name}" đã được xóa thành công.', 'success')
    return redirect(url_for('product.manage'))
