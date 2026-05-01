from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục.'
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    with app.app_context():
        # Import models
        from app.models.user import User
        from app.models.product import Product, Category
        from app.models.order import Order, OrderItem
        from app.models.review import Review
        
        # Create database tables
        db.create_all()
        
        # Register blueprints
        from app.routes.main import main_bp
        from app.routes.auth import auth_bp
        from app.routes.product import product_bp
        from app.routes.cart import cart_bp
        from app.routes.order import order_bp
        from app.routes.admin import admin_bp
        from app.routes.user import user_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(product_bp, url_prefix='/products')
        app.register_blueprint(cart_bp, url_prefix='/cart')
        app.register_blueprint(order_bp, url_prefix='/orders')
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(user_bp, url_prefix='/user')
        
        # Setup login manager
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
    
    return app
