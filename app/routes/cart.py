from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/')
def view_cart():
    """View shopping cart"""
    cart = session.get('cart', {})
    from app.models.product import Product
    
    items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
            total += product.price * quantity
    
    return render_template('cart/view.html', items=items, total=total)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add product to cart"""
    from app.models.product import Product
    
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity', 1, type=int)
    
    if not product.is_in_stock():
        flash('Sản phẩm hết hàng.', 'danger')
        return redirect(request.referrer or url_for('main.index'))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity
    
    session.modified = True
    flash(f'Đã thêm {product.name} vào giỏ hàng.', 'success')
    
    return redirect(request.referrer or url_for('main.index'))

@cart_bp.route('/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    """Update cart item quantity"""
    quantity = request.form.get('quantity', 0, type=int)
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if quantity <= 0:
        session['cart'].pop(str(product_id), None)
        flash('Sản phẩm đã được xóa khỏi giỏ hàng.', 'success')
    else:
        session['cart'][str(product_id)] = quantity
        flash('Giỏ hàng đã được cập nhật.', 'success')
    
    session.modified = True
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Remove product from cart"""
    if 'cart' in session:
        session['cart'].pop(str(product_id), None)
        session.modified = True
    
    flash('Sản phẩm đã được xóa khỏi giỏ hàng.', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    """Clear entire cart"""
    session['cart'] = {}
    session.modified = True
    flash('Giỏ hàng đã được xóa.', 'success')
    return redirect(url_for('main.index'))
