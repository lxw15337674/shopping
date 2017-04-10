from flask import g
from flask import render_template, session, redirect, url_for
from flask import flash
from flask_login import login_user, logout_user, login_required, current_user

from app import app, lm, db
from app.forms import LoginForm, RegisterForm, UploadForm, SearchForm
from app.models import User, Fruits


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/goods')
# @app.route('/goods/<int:pages>')
# def goods(page=1):
#     fruits = Fruits.query.filter_by().all()
#     posts = fruits.paginate(page, POSTS_PER_PAGE, False)

@app.route('/goods', methods=['GET', 'POST'])
def goods():
    form = SearchForm()
    fruits = Fruits.query.filter_by().all()
    if form.validate_on_submit():
        print(123)
        return redirect(url_for('search_results', query=form.search.data))
    return render_template('goods.html', title="商品", fruits=fruits,form=form)


# 管理员上传水果商品信息
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        fruit = Fruits(name=form.name.data, introduction=form.introduction.data, price=form.price.data)
        db.session.add(fruit)
        db.session.commit()
        flash('上传成功')
        return redirect(url_for('upload'))
    return render_template('upload.html', title="上传", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    searchform = SearchForm()
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
    if searchform.validate_on_submit():
        return redirect(url_for('search_results', query=searchform.search.data))
    return render_template('login.html', title="登录", form=form)


# 搜索功能
@app.route('/search_results/<query>' )
@login_required
def search_results(query):
    results = Fruits.query.filter_by(name=query).all()
    return render_template('search_results.html',
                           results=results)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.name.data,
                    password=form.password1.data,
                    address=form.address.data,
                    sex=form.sex.data,
                    phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('login'))
    return render_template('register.html', title="注册", form=form)


# 登出
@login_required
@app.route('/logout')
def logout():
    logout_user()
    flash("登出成功")
    return redirect(url_for('login'))


# 设置请求前的全局用户
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
