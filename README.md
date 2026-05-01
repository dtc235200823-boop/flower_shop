# 🌸 Cửa Hàng Hoa Tươi - Flower Shop

Website bán hoa tươi được xây dựng bằng Python Flask với đầy đủ chức năng quản lý sản phẩm, đơn hàng, người dùng và thống kê.

## 📋 Mục Tiêu Dự Án

Xây dựng một ứng dụng web hoàn chỉnh để quản lý bán hàng hoa tươi với các tính năng:
- ✅ Xác thực & phân quyền người dùng
- ✅ CRUD cho sản phẩm, danh mục, người dùng
- ✅ Quản lý đơn hàng (trạng thái, thanh toán)
- ✅ Giỏ hàng và thanh toán
- ✅ Đánh giá & bình luận sản phẩm
- ✅ Tìm kiếm, lọc, sắp xếp sản phẩm
- ✅ Dashboard quản trị với thống kê
- ✅ Upload ảnh sản phẩm
- ✅ Phân quyền theo vai trò (Khách, Người dùng, Quản trị)

## 🏗️ Kiến Trúc Hệ Thống

### Công Nghệ Sử Dụng
- **Backend:** Python 3.9+ với Flask
- **Database:** SQLite (mặc định), hỗ trợ MySQL
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login
- **Form Validation:** WTForms

### Cấu Trúc Thư Mục
```
flower_shop/
├── app/
│   ├── models/              # Các model database
│   │   ├── user.py         # Model người dùng
│   │   ├── product.py      # Model sản phẩm
│   │   ├── order.py        # Model đơn hàng
│   │   └── review.py       # Model đánh giá
│   ├── routes/             # Các route/endpoint
│   │   ├── main.py         # Trang chính
│   │   ├── auth.py         # Xác thực
│   │   ├── product.py      # Sản phẩm
│   │   ├── order.py        # Đơn hàng
│   │   ├── cart.py         # Giỏ hàng
│   │   ├── admin.py        # Quản trị
│   │   └── user.py         # Người dùng
│   ├── forms/              # Các form
│   │   ├── auth.py
│   │   ├── product.py
│   │   └── order.py
│   ├── templates/          # HTML templates
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/        # Thư mục upload ảnh
│   └── __init__.py
├── config.py               # Cấu hình ứng dụng
├── run.py                  # File chạy ứng dụng
├── requirements.txt        # Các dependency
└── README.md
```

## 📦 Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.9 hoặc cao hơn
- pip (Package manager Python)
- Git (tùy chọn)

### Các Bước Cài Đặt

1. **Clone hoặc tải project**
   ```bash
   cd d:\Dự án w\flower_shop
   ```

2. **Tạo Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Cài đặt Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Khởi Tạo Database**
   ```bash
   python run.py
   ```

5. **Seed Sample Data**
   ```bash
   flask seed-db
   ```

## 🚀 Chạy Ứng Dụng

### Mode Development
```bash
python run.py
```

Truy cập: `http://localhost:5000`

### Mode Production
```bash
flask run --host=0.0.0.0 --port=8000
```

## 👤 Tài Khoản Mẫu

Sau khi chạy `flask seed-db`, bạn có thể sử dụng:

### Admin Account
- **Username:** admin
- **Password:** admin123
- **Email:** admin@flowershop.local

### Customer Account
- **Username:** customer
- **Password:** customer123
- **Email:** customer@flowershop.local

## 📊 Các Chức Năng Chính

### 1. Xác Thực & Phân Quyền
- [x] Đăng ký tài khoản
- [x] Đăng nhập
- [x] Quên mật khẩu
- [x] Phân quyền theo vai trò (Customer, Staff, Admin)

### 2. Quản Lý Sản Phẩm (CRUD)
- [x] Xem danh sách sản phẩm
- [x] Xem chi tiết sản phẩm
- [x] Thêm sản phẩm (Admin)
- [x] Sửa sản phẩm (Admin)
- [x] Xóa sản phẩm (Admin)
- [x] Upload ảnh sản phẩm
- [x] Danh mục sản phẩm

### 3. Tìm Kiếm & Lọc
- [x] Tìm kiếm theo tên
- [x] Lọc theo danh mục
- [x] Sắp xếp (giá, đánh giá, phổ biến)
- [x] Phân trang

### 4. Giỏ Hàng & Đặt Hàng
- [x] Thêm sản phẩm vào giỏ
- [x] Cập nhật số lượng
- [x] Xóa sản phẩm khỏi giỏ
- [x] Thanh toán (Checkout)
- [x] Xem đơn hàng

### 5. Quản Lý Đơn Hàng
- [x] Tạo đơn hàng
- [x] Xem trạng thái đơn hàng
- [x] Cập nhật trạng thái (Admin)
- [x] Xóa/Hủy đơn hàng
- [x] Theo dõi thanh toán

### 6. Đánh Giá & Bình Luận
- [x] Đánh giá sản phẩm (1-5 sao)
- [x] Viết bình luận
- [x] Duyệt bình luận (Admin)

### 7. Quản Trị & Thống Kê
- [x] Dashboard quản trị
- [x] Thống kê đơn hàng
- [x] Thống kê doanh thu
- [x] Quản lý người dùng
- [x] Báo cáo sản phẩm bán chạy
- [x] Quản lý danh mục

## 🗄️ Cấu Trúc Database

### Bảng Users
```
id (PK)
username (UNIQUE)
email (UNIQUE)
password_hash
full_name
phone
address
city
postal_code
role (customer, staff, admin)
avatar
is_active
created_at
updated_at
```

### Bảng Products
```
id (PK)
name
description
category_id (FK)
price
stock
image
color
quantity_per_item
origin
is_active
is_featured
rating
view_count
created_at
updated_at
```

### Bảng Orders
```
id (PK)
order_number (UNIQUE)
user_id (FK)
status (pending, confirmed, processing, shipped, delivered, cancelled)
payment_status (pending, paid, failed, refunded)
total_amount
tax
shipping_cost
discount
delivery_address
delivery_city
delivery_postal_code
delivery_phone
delivery_date
notes
created_at
updated_at
```

### Bảng OrderItems
```
id (PK)
order_id (FK)
product_id (FK)
quantity
unit_price
total_price
```

### Bảng Reviews
```
id (PK)
product_id (FK)
user_id (FK)
rating (1-5)
title
comment
is_approved
created_at
updated_at
```

### Bảng Categories
```
id (PK)
name (UNIQUE)
description
image
is_active
created_at
```

## 📝 Các Endpoint Chính

### Trang Chính
- `GET /` - Trang chủ
- `GET /about` - Về chúng tôi
- `GET /contact` - Liên hệ
- `POST /contact` - Gửi tin nhắn liên hệ

### Authentication
- `GET/POST /auth/register` - Đăng ký
- `GET/POST /auth/login` - Đăng nhập
- `GET /auth/logout` - Đăng xuất
- `GET/POST /auth/profile` - Hồ sơ người dùng
- `GET/POST /auth/change-password` - Đổi mật khẩu

### Sản Phẩm
- `GET /products/` - Danh sách sản phẩm
- `GET /products/<id>` - Chi tiết sản phẩm
- `POST /products/<id>/review` - Thêm đánh giá
- `GET /search` - Tìm kiếm sản phẩm

### Giỏ Hàng
- `GET /cart/` - Xem giỏ hàng
- `POST /cart/add/<id>` - Thêm vào giỏ
- `POST /cart/update/<id>` - Cập nhật số lượng
- `POST /cart/remove/<id>` - Xóa khỏi giỏ
- `POST /cart/clear` - Xóa toàn bộ giỏ

### Đơn Hàng
- `GET /orders/` - Đơn hàng của tôi
- `GET /orders/<id>` - Chi tiết đơn hàng
- `GET/POST /orders/checkout` - Thanh toán
- `POST /orders/<id>/cancel` - Hủy đơn hàng

### Admin
- `GET /admin/` - Dashboard
- `GET /admin/products` - Quản lý sản phẩm
- `GET/POST /admin/products/create` - Thêm sản phẩm
- `GET/POST /admin/products/<id>/edit` - Sửa sản phẩm
- `POST /admin/products/<id>/delete` - Xóa sản phẩm
- `GET /admin/users` - Quản lý người dùng
- `GET /admin/orders` - Quản lý đơn hàng
- `GET /admin/categories` - Quản lý danh mục
- `GET /admin/reports` - Báo cáo thống kê

## 🔒 Bảo Mật

- Mật khẩu được mã hóa bằng Werkzeug
- Session được bảo vệ
- CSRF protection với WTForms
- Kiểm tra quyền truy cập ở mỗi endpoint
- Kiểm tra kích thước & định dạng file upload

## 📱 Responsive Design

Ứng dụng hỗ trợ đầy đủ:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🐛 Khắc Phục Sự Cố

### Lỗi: Module not found
```bash
pip install -r requirements.txt
```

### Lỗi: Database locked
Xóa file `flower_shop.db` và chạy lại:
```bash
python run.py
flask seed-db
```

### Lỗi: Upload ảnh không hoạt động
Kiểm tra thư mục `app/static/uploads/` có tồn tại không

## 🚀 Triển Khai Production

1. **Cài đặt Production Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 run:app
   ```

2. **Sử dụng MySQL thay SQLite**
   - Cập nhật `DATABASE_URL` trong `.env`
   - Chạy migration database

3. **Bảo mật SSL**
   - Sử dụng Nginx reverse proxy
   - Cấu hình SSL certificate

## 📚 Tài Liệu Thêm

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Flask-Login](https://flask-login.readthedocs.io/)

## 👨‍💻 Đội Phát Triển

- **Tác Giả:** [Your Name]
- **Dự Án:** Flower Shop - Bán Hoa Tươi
- **Năm:** 2024

## 📄 Giấy Phép

Dự án này được phát hành dưới giấy phép MIT.

## 📞 Hỗ Trợ

Nếu gặp vấn đề, vui lòng tạo Issue trên GitHub hoặc liên hệ:
- Email: support@flowershop.vn
- Phone: 1900-1234
- Website: www.flowershop.vn

---

**Cảm ơn bạn đã sử dụng Flower Shop! 🌸**
