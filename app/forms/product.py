from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.widgets import TextArea

class ProductForm(FlaskForm):
    """Product form for CRUD"""
    name = StringField('Tên sản phẩm', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Mô tả', render_kw={"rows": 5})
    category_id = SelectField('Danh mục', coerce=int, validators=[DataRequired()])
    price = FloatField('Giá bán', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Số lượng', validators=[DataRequired(), NumberRange(min=0)])
    color = StringField('Màu sắc')
    quantity_per_item = StringField('Số lượng mỗi đơn vị (vd: 10 bông)')
    origin = StringField('Xuất xứ')
    image = FileField('Ảnh sản phẩm')
    is_featured = BooleanField('Sản phẩm nổi bật')
    is_active = BooleanField('Kích hoạt', default=True)
    submit = SubmitField('Lưu sản phẩm')

class CategoryForm(FlaskForm):
    """Category form"""
    name = StringField('Tên danh mục', validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField('Mô tả')
    image = FileField('Ảnh danh mục')
    is_active = BooleanField('Kích hoạt', default=True)
    submit = SubmitField('Lưu danh mục')

class ReviewForm(FlaskForm):
    """Product review form"""
    rating = SelectField('Đánh giá', coerce=int, choices=[
        (5, '⭐⭐⭐⭐⭐ Rất tốt'),
        (4, '⭐⭐⭐⭐ Tốt'),
        (3, '⭐⭐⭐ Bình thường'),
        (2, '⭐⭐ Không tốt'),
        (1, '⭐ Rất không tốt')
    ], validators=[DataRequired()])
    title = StringField('Tiêu đề', validators=[DataRequired(), Length(min=3, max=200)])
    comment = TextAreaField('Bình luận', validators=[Optional(), Length(min=5)])
    submit = SubmitField('Gửi đánh giá')

class SearchForm(FlaskForm):
    """Search form"""
    query = StringField('Tìm kiếm', validators=[DataRequired()])
    category_id = SelectField('Danh mục', coerce=int, choices=[], validators=[Optional()])
    sort_by = SelectField('Sắp xếp', choices=[
        ('newest', 'Mới nhất'),
        ('price_asc', 'Giá: Thấp → Cao'),
        ('price_desc', 'Giá: Cao → Thấp'),
        ('rating', 'Đánh giá cao nhất'),
        ('popular', 'Phổ biến nhất')
    ])
    submit = SubmitField('Tìm kiếm')
