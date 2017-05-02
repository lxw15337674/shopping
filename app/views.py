from flask import g
from flask import render_template, redirect, url_for
from flask import flash
from flask_login import login_user, logout_user, login_required, current_user

from app import app, lm, db, date, adminpassword
from app.forms import LoginForm, RegisterForm, UploadForm, SearchForm
from app.models import User, Fruits, Order, OrderItem


@app.route('/')
def index():
    fruits = Fruits.query.filter_by().order_by(Fruits.id.desc()).limit(4).all()
    return render_template('index.html', fruits=fruits)


# 管理员查看用户页面
@app.route('/admin')
@login_required
def admin():
    if g.user.is_admin():
        flash("管理员你好")
    else:
        flash("不是管理员,不能进入该页面")
        return redirect(url_for('goods'))
    alluser = User.query.filter_by().all()
    return render_template('admin.html',alluser=alluser)

# 管理员查看商品页面
@app.route('/admin_fruit')
@login_required
def admin_fruit():
    if g.user.is_admin():
        flash("管理员你好")
    else:
        flash("不是管理员,不能进入该页面")
        return redirect(url_for('goods'))
    allfruit = Fruits.query.filter_by().all()
    return render_template('admin_fruit.html',allfruit=allfruit)

# 管理员查看订单页面
@app.route('/admin_order')
@login_required
def admin_order():
    if g.user.is_admin():
        flash("管理员你好")
    else:
        flash("不是管理员,不能进入该页面")
        return redirect(url_for('goods'))
    allorder = Order.query.filter_by().all()
    return render_template('admin_order.html',allorder=allorder)

# 商品列表
@app.route('/goods', methods=['GET', 'POST'])
def goods():
    form = SearchForm()
    fruits = Fruits.query.filter_by().all()
    if form.validate_on_submit():
        return redirect(url_for('search_results', query=form.search.data))
    return render_template('goods.html', title="商品", fruits=fruits, form=form)


# 商品详细信息(购买页面)
@app.route('/fruit/<id>')
def fruit(id):
    fruit = Fruits.query.filter_by(id=id).first()
    if fruit is None:
        flash("不存在该商品")
        return redirect(url_for('goods'))
    return render_template('fruit.html', fruit=fruit)


# 加入购物车
@app.route('/cart/<id>')
@login_required
def cart(id, num=1):
    order = Order.query.filter_by(user_id=g.user.id, status='购物车').first()  # 购物车
    # 如果购物车中存在该商品则直接更新数量,如果不存在则增加该商品
    target = int(id)
    for a in order.items:
        if target == a.fruit_id:
            a.changenum(num)  # 更新订单商品数量
            order.updatecost()  # 更新订单价格
            db.session.commit()
            flash('已增加数量')
            return redirect(url_for('fruit', id=id))
    orderitem = OrderItem()
    orderitem.add(fruit_id=id, num=num, order_id=order.id)
    db.session.add(orderitem)
    order.updatecost()  # 更新订单价格
    db.session.commit()
    flash('已加入购物车')
    return redirect(url_for('fruit', id=id))


# 查看购物车
@app.route('/buy')
@login_required
def buy():
    order = Order.query.filter_by(user_id=g.user.id, status='购物车').first()  # 购物车
    return render_template('buy.html', order=order)


@app.route('/pay/<id>')
@login_required
def pay(id):
    order = Order.query.filter_by(id=id).first()  # 购物车
    order.status = '完成'
    db.session.commit()
    flash("订单完成")
    return render_template('order.html', order=order)


# 用于显示订单
@app.route('/list')
@login_required
def list():
    user = User.query.filter_by(id=g.user.id).first()
    return render_template('list.html', user=user)


# 结算
@app.route('/order/<id>')
@login_required
def order(id):
    order = Order.query.filter_by(id=id).first()
    if order.status == '购物车':
        order.status = '未支付'
        order.time = date.date()
        order.address = User.query.filter_by(id=g.user.id).first().address
        db.session.commit()
        flash('已提交')
        # 再给用户创建购物车
        order = Order(g.user.id)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('order', id=id))
    return render_template('order.html', order=order)


# 购物车页面改变商品数量
@app.route('/changenum/<id>/<num>', methods=['GET'])
@login_required
def changenum(id, num):
    fruit = OrderItem.query.filter_by(id=id).first()
    num = int(num)
    fruit.changenum(num)  # 更新订单商品数量
    if fruit.num <= 0:
        db.session.delete(fruit)
    order = Order.query.filter_by(id=fruit.Order_id).first()  # 购物车
    order.updatecost()  # 更新订单价格
    db.session.commit()
    return redirect(url_for('buy'))


# 管理员上传水果商品信息
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if g.user.is_admin():
        pass
    else:
        flash("不是管理员,不能进入该页面")
        return redirect(url_for('goods'))
    form = UploadForm()
    if form.validate_on_submit():
        fruit = Fruits(name=form.name.data, introduction=form.introduction.data, price=form.price.data,
                       photo=form.photo.data)
        db.session.add(fruit)
        db.session.commit()
        flash('上传成功')
        return redirect(url_for('upload'))

    return render_template('upload.html', title="上传", form=form)


# 登录
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
            # 初始化,创建购物车
            if Order.query.filter_by(user_id=g.user.id, status='购物车').first() is None:
                order = Order(g.user.id)
                db.session.add(order)
                db.session.commit()
            flash("登陆成功")
            return redirect(url_for("goods"))
    if searchform.validate_on_submit():
        return redirect(url_for('search_results', query=searchform.search.data))
    return render_template('login.html', title="登录", form=form)


# 搜索功能
@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Fruits.query.filter_by(name=query).all()
    return render_template('search_results.html',
                           results=results)

# 购物车页面改变商品数量
@app.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
    fruit = Fruits.query.filter_by(id=id).first()
    if fruit:
        db.session.delete(fruit)
        db.session.commit()
        flash("删除成功")
    return redirect(url_for('admin_fruit'))

# 注册功能
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.admin.data == adminpassword:
            admin = True
        else:
            admin= False
        user = User(email=form.email.data,
                    name=form.name.data,
                    password=form.password1.data,
                    address=form.address.data,
                    sex=form.sex.data,
                    phone=form.phone.data,
                    admin=admin)
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
