from flask import Blueprint, render_template, request, current_app
from app import db
from app.models.product import Product, Category
from app.models.order import Order

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    page = request.args.get('page', 1, type=int)
    featured_products = Product.query.filter_by(is_featured=True, is_active=True).limit(6).all()
    products = Product.query.filter_by(is_active=True).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE']
    )
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('index.html', 
                         featured_products=featured_products,
                         products=products,
                         categories=categories)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        # Handle contact form submission
        return render_template('contact.html', message='Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất.')
    return render_template('contact.html')

@main_bp.route('/search')
def search():
    """Search products"""
    query = request.args.get('q', '')
    category_id = request.args.get('category', 0, type=int)
    sort_by = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    
    search_query = Product.query.filter_by(is_active=True)
    
    if query:
        search_query = search_query.filter(
            (Product.name.ilike(f'%{query}%')) |
            (Product.description.ilike(f'%{query}%'))
        )
    
    if category_id:
        search_query = search_query.filter_by(category_id=category_id)
    
    # Apply sorting
    if sort_by == 'price_asc':
        search_query = search_query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        search_query = search_query.order_by(Product.price.desc())
    elif sort_by == 'rating':
        search_query = search_query.order_by(Product.rating.desc())
    elif sort_by == 'popular':
        search_query = search_query.order_by(Product.view_count.desc())
    else:  # newest
        search_query = search_query.order_by(Product.created_at.desc())
    
    products = search_query.paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE']
    )
    
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('search.html',
                         query=query,
                         products=products,
                         categories=categories,
                         current_category=category_id,
                         sort_by=sort_by)

@main_bp.route('/dashboard')
def dashboard():
    """Admin/User dashboard"""
    from flask_login import current_user, login_required
    
    @login_required
    def _dashboard():
        if current_user.is_admin():
            # Admin dashboard
            total_orders = Order.query.count()
            total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
            pending_orders = Order.query.filter_by(status='pending').count()
            products_count = Product.query.count()
            
            recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
            
            return render_template('dashboard.html',
                                 total_orders=total_orders,
                                 total_revenue=total_revenue,
                                 pending_orders=pending_orders,
                                 products_count=products_count,
                                 recent_orders=recent_orders)
        else:
            # User dashboard
            user_orders = Order.query.filter_by(user_id=current_user.id).all()
            return render_template('user_dashboard.html',
                                 orders=user_orders)
    
    return _dashboard()
