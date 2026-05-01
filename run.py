import os
from app import create_app, db
from app.models.user import User
from app.models.product import Product, Category, Inventory
from app.models.order import Order, OrderItem
from app.models.review import Review

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Category': Category,
        'Order': Order,
        'OrderItem': OrderItem,
        'Review': Review,
        'Inventory': Inventory
    }

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    # Create categories
    categories = [
        Category(name='Hoa Hồng', description='Những bông hoa hồng tươi, đẹp'),
        Category(name='Hoa Lạ', description='Những loại hoa hiếm từ khắp nơi'),
        Category(name='Hoa Mặt Trời', description='Hoa mặt trời rực rỡ'),
        Category(name='Hoa Tulip', description='Hoa tulip đa sắc'),
        Category(name='Bó Hoa Kỷ Niệm', description='Bó hoa cho các dịp đặc biệt'),
    ]
    
    for cat in categories:
        if not Category.query.filter_by(name=cat.name).first():
            db.session.add(cat)
    
    db.session.commit()
    
    # Create products
    products_data = [
        {
            'name': 'Bó Hoa Hồng Đỏ 12 Bông',
            'category_name': 'Hoa Hồng',
            'price': 250000,
            'stock': 50,
            'color': 'Đỏ',
            'quantity_per_item': '12 bông',
            'origin': 'Việt Nam'
        },
        {
            'name': 'Bó Hoa Hồng Trắng 15 Bông',
            'category_name': 'Hoa Hồng',
            'price': 300000,
            'stock': 40,
            'color': 'Trắng',
            'quantity_per_item': '15 bông',
            'origin': 'Việt Nam'
        },
        {
            'name': 'Hoa Hướng Dương Khổng Lồ',
            'category_name': 'Hoa Mặt Trời',
            'price': 180000,
            'stock': 30,
            'color': 'Vàng',
            'quantity_per_item': '1 bó',
            'origin': 'Việt Nam'
        },
        {
            'name': 'Bó Hoa Tulip Đa Màu',
            'category_name': 'Hoa Tulip',
            'price': 350000,
            'stock': 25,
            'color': 'Đa màu',
            'quantity_per_item': '20 bông',
            'origin': 'Hà Lan'
        },
        {
            'name': 'Bó Hoa Kỷ Niệm Sang Trọng',
            'category_name': 'Bó Hoa Kỷ Niệm',
            'price': 500000,
            'stock': 15,
            'color': 'Kết hợp',
            'quantity_per_item': '30 bông',
            'origin': 'Việt Nam'
        },
    ]
    
    for data in products_data:
        if not Product.query.filter_by(name=data['name']).first():
            category = Category.query.filter_by(name=data['category_name']).first()
            product = Product(
                name=data['name'],
                category_id=category.id,
                price=data['price'],
                stock=data['stock'],
                color=data['color'],
                quantity_per_item=data['quantity_per_item'],
                origin=data['origin'],
                is_active=True,
                is_featured=True
            )
            db.session.add(product)
    
    db.session.commit()
    
    # Create admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@flowershop.local',
            full_name='Administrator',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Create test user
    if not User.query.filter_by(username='customer').first():
        customer = User(
            username='customer',
            email='customer@flowershop.local',
            full_name='Test Customer',
            phone='0901234567',
            address='123 Đường Ngô Quyền',
            city='Hà Nội',
            postal_code='100000',
            role='customer',
            is_active=True
        )
        customer.set_password('customer123')
        db.session.add(customer)
    
    db.session.commit()
    print('Database seeded with sample data!')

if __name__ == '__main__':
    app.run(debug=True)
