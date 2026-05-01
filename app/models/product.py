from app import db
from datetime import datetime

class Category(db.Model):
    """Product category model"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    """Product model"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image = db.Column(db.String(255))
    color = db.Column(db.String(100))
    quantity_per_item = db.Column(db.String(100))  # Ví dụ: "10 bông", "1 bó"
    origin = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')
    inventory = db.relationship('Inventory', backref='product', lazy=False, uselist=False, cascade='all, delete-orphan')
    
    def get_rating(self):
        """Get average rating"""
        if not self.reviews:
            return 0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)
    
    def get_review_count(self):
        """Get number of reviews"""
        return len(self.reviews)
    
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Inventory(db.Model):
    """Inventory tracking model"""
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, unique=True)
    quantity_available = db.Column(db.Integer, default=0)
    quantity_reserved = db.Column(db.Integer, default=0)
    last_restocked = db.Column(db.DateTime)
    low_stock_threshold = db.Column(db.Integer, default=5)
    
    def get_available_quantity(self):
        """Get available quantity (available - reserved)"""
        return max(0, self.quantity_available - self.quantity_reserved)
    
    def __repr__(self):
        return f'<Inventory Product:{self.product_id} Available:{self.quantity_available}>'
