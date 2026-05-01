from app import db
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    """Order status enum"""
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class PaymentStatus(Enum):
    """Payment status enum"""
    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'
    REFUNDED = 'refunded'

class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default=OrderStatus.PENDING.value)
    payment_status = db.Column(db.String(20), default=PaymentStatus.PENDING.value)
    total_amount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, default=0)
    shipping_cost = db.Column(db.Float, default=0)
    discount = db.Column(db.Float, default=0)
    
    # Delivery info
    delivery_address = db.Column(db.Text, nullable=False)
    delivery_city = db.Column(db.String(120))
    delivery_postal_code = db.Column(db.String(10))
    delivery_phone = db.Column(db.String(20))
    delivery_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def calculate_total(self):
        """Calculate total amount"""
        subtotal = sum(item.total_price for item in self.items)
        self.total_amount = subtotal + self.tax + self.shipping_cost - self.discount
        return self.total_amount
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    """Order item model (chi tiết đơn hàng)"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    
    def calculate_total(self):
        """Calculate item total price"""
        self.total_price = self.quantity * self.unit_price
        return self.total_price
    
    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Product:{self.product_id}>'
