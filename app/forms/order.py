from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, Optional, Email

class CheckoutForm(FlaskForm):
    """Checkout form"""
    delivery_address = TextAreaField('Địa chỉ giao hàng', validators=[DataRequired(), Length(min=5)])
    delivery_city = StringField('Thành phố', validators=[DataRequired()])
    delivery_postal_code = StringField('Mã bưu điện', validators=[DataRequired()])
    delivery_phone = StringField('Số điện thoại', validators=[DataRequired()])
    notes = TextAreaField('Ghi chú đơn hàng', validators=[Optional()])
    payment_method = SelectField('Phương thức thanh toán', choices=[
        ('cod', 'Thanh toán khi nhận hàng'),
        ('bank', 'Chuyển khoản ngân hàng'),
        ('card', 'Thẻ tín dụng')
    ], validators=[DataRequired()])
    submit = SubmitField('Hoàn thành đặt hàng')

class OrderStatusForm(FlaskForm):
    """Update order status form (for admin)"""
    status = SelectField('Trạng thái đơn hàng', choices=[
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã gửi'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy')
    ], validators=[DataRequired()])
    payment_status = SelectField('Trạng thái thanh toán', choices=[
        ('pending', 'Chưa thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('failed', 'Thanh toán thất bại'),
        ('refunded', 'Đã hoàn lại')
    ], validators=[DataRequired()])
    notes = TextAreaField('Ghi chú')
    submit = SubmitField('Cập nhật trạng thái')
