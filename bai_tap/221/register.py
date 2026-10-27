from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    DataRequired, Length, Regexp, Email, EqualTo
)


class RegisterForm(FlaskForm):
    username = StringField(
        "Tên đăng nhập",
        validators=[
            DataRequired(message="Vui lòng nhập tên đăng nhập."),
            Length(min=4, max=20,
                   message="Tên đăng nhập phải từ 4 đến 20 ký tự."),
            Regexp(
                r"^[a-z0-9_]+$",
                message="Chỉ được dùng chữ thường không dấu, số và dấu gạch dưới (_)."
            )
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Vui lòng nhập email."),
            Email(message="Email không đúng định dạng.")
        ]
    )
    password = PasswordField(
        "Mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập mật khẩu."),
            Length(min=8, message="Mật khẩu phải có ít nhất 8 ký tự.")
        ]
    )
    confirm_password = PasswordField(
        "Nhập lại mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập lại mật khẩu."),
            EqualTo("password", message="Mật khẩu nhập lại không khớp.")
        ]
    )
    terms = BooleanField(
        "Tôi đồng ý với các điều khoản",
        validators=[
            DataRequired(message="Bạn phải đồng ý với các điều khoản.")
        ]
    )
    submit = SubmitField("Đăng ký")