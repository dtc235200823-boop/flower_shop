from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from datetime import datetime
import uuid
from app import db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.forms.order import CheckoutForm, OrderStatusForm

order_bp = Blueprint('order', __name__)

@order_bp.route('/')
@login_required
def my_orders():
    """View user's orders"""
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(user_id=current_user.id).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE']
    )
    
    return render_template('orders/my_orders.html', orders=orders)

@order_bp.route('/<int:order_id>')
@login_required
def view_order(order_id):
    """View order details"""
    order = Order.query.get_or_404(order_id)
    
    # Check if user has permission to view this order
    if order.user_id != current_user.id and not current_user.is_admin():
        flash('Bạn không có quyền xem đơn hàng này.', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('orders/view_order.html', order=order)

@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout"""
    from flask import session
    
    # Get cart from session
    cart = session.get('cart', {})
    if not cart:
        flash('Giỏ hàng trống.', 'warning')
        return redirect(url_for('main.index'))
    
    form = CheckoutForm()
    
    if form.validate_on_submit():
        # Create order
        order = Order(
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            user_id=current_user.id,
            delivery_address=form.delivery_address.data,
            delivery_city=form.delivery_city.data,
            delivery_postal_code=form.delivery_postal_code.data,
            delivery_phone=form.delivery_phone.data,
            notes=form.notes.data
        )
        
        total = 0
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                item = OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price
                )
                item.calculate_total()
                order.items.append(item)
                
                # Update product stock
                product.stock -= quantity
                total += item.total_price
        
        order.total_amount = total
        order.shipping_cost = 30000  # Fixed shipping cost
        order.total_amount += order.shipping_cost
        
        db.session.add(order)
        db.session.commit()
        
        # Clear cart
        from flask import session
        session['cart'] = {}
        session.modified = True
        
        flash('Đơn hàng đã được tạo thành công!', 'success')
        return redirect(url_for('order.view_order', order_id=order.id))
    
    # Populate form with current user info
    if request.method == 'GET':
        form.delivery_address.data = current_user.address or ''
        form.delivery_city.data = current_user.city or ''
        form.delivery_postal_code.data = current_user.postal_code or ''
        form.delivery_phone.data = current_user.phone or ''
    
    # Calculate cart items
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
    
    return render_template('orders/checkout.html', 
                         form=form, 
                         items=items, 
                         total=total)

# Admin routes
@order_bp.route('/manage')
@login_required
def manage():
    """Manage orders (admin only)"""
    if not current_user.is_admin():
        flash('Bạn không có quyền truy cập.', 'danger')
        return redirect(url_for('main.index'))
    
    status = request.args.get('status', 'all')
    page = request.args.get('page', 1, type=int)
    
    query = Order.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE']
    )
    
    return render_template('admin/orders/list.html', orders=orders, current_status=status)

@order_bp.route('/<int:order_id>/update-status', methods=['POST'])
@login_required
def update_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    
    if not current_user.is_admin():
        flash('Bạn không có quyền truy cập.', 'danger')
        return redirect(url_for('main.index'))
    
    form = OrderStatusForm()
    if form.validate_on_submit():
        order.status = form.status.data
        order.payment_status = form.payment_status.data
        order.notes = form.notes.data or order.notes
        db.session.commit()
        
        flash('Trạng thái đơn hàng đã được cập nhật.', 'success')
    
    return redirect(url_for('order.view_order', order_id=order_id))

@order_bp.route('/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Cancel order"""
    order = Order.query.get_or_404(order_id)
    
    # Check if user has permission
    if order.user_id != current_user.id and not current_user.is_admin():
        flash('Bạn không có quyền hủy đơn hàng này.', 'danger')
        return redirect(url_for('main.index'))
    
    if order.status not in ['pending', 'confirmed']:
        flash('Không thể hủy đơn hàng ở trạng thái này.', 'warning')
        return redirect(url_for('order.view_order', order_id=order_id))
    
    # Restore product stock
    for item in order.items:
        item.product.stock += item.quantity
    
    order.status = 'cancelled'
    db.session.commit()
    
    flash('Đơn hàng đã được hủy.', 'success')
    return redirect(url_for('order.view_order', order_id=order_id))
