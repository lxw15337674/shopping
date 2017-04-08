from flask import g
from flask import render_template, session, redirect, url_for
from flask import flash
from flask_login import login_user, logout_user,login_required,current_user

from app import app, lm
from app.forms import LoginForm
from app.models import User


@app.route('/')
def index():
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        user = User.query.filter_by(name=name).first()
        if not user:
            flash('该用户不存在')
        elif user.password != form.password.data:
            flash('密码错误')
        else:
            login_user(user, form.remember_me.data)
            flash("登陆成功")
            return redirect(url_for("index"))
    return render_template('login.html', title="登录", form=form)


# 登出
@login_required
@app.route('/logout')
def logout():
    logout_user()
    flash("登出成功")
    return redirect(url_for('login'))

#设置请求前的全局用户
@app.before_request
def before_request():
    g.user = current_user

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
