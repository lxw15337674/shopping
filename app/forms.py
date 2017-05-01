from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, RadioField, FileField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, Email, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired(message="不能为空")])
    password = PasswordField('密码', validators=[DataRequired(message="不能为空")])
    remember_me = BooleanField('记住登录状态', default=False)
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired()])
    password1 = PasswordField('密码', validators=[
        DataRequired(message="不能为空"), EqualTo('password2', message='密码必须相同.')])
    password2 = PasswordField('再次输入密码', validators=[DataRequired(message="不能为空")])
    address = StringField('地址', validators=[DataRequired(message="不能为空")])
    sex = RadioField('性别', choices=[('男', '男'), ('女', '女')], validators=[DataRequired(message="必须选择")])
    phone = StringField('手机号', validators=[DataRequired(message="不能为空"), Length(11, 11, message="必须为11位数字"),
                                           Regexp('[0-9]*', message='必须为数字')])
    email = StringField('邮箱', validators=[DataRequired(message="不能为空"), Email(message="请输入正确的邮箱格式")])
    admin = StringField('注册管理员密码(用户不用输入该栏)')
    submit = SubmitField('提交')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已经被使用.')


class UploadForm(FlaskForm):
    name = StringField('商品名称', validators=[DataRequired(message="不能为空")])
    photo = StringField('商品图片', validators=[DataRequired(message="不能为空")])
    introduction = StringField('商品介绍', validators=[DataRequired(message="不能为空")])
    price = StringField('商品价格', validators=[DataRequired(message="不能为空"), Regexp('[0-9]*', message='必须为数字')])
    submit = SubmitField('提交')


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired(message="搜索不能为空")])
    submit = SubmitField('搜索')
