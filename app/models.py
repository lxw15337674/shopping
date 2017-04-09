from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64))
    sex = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    is_admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, name, password,address,sex,phone,email):
        self.name = name
        self.password = password
        self.address = address
        self.sex = sex
        self.phone = phone
        self.email = email

    # 是否被认证
    def is_authenticated(self):
        return True

    # 是否有效,除非用户被禁止
    def is_active(self):
        return True

    # 是否匿名
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Fruits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    introduction = db.Column(db.String(1000))
    photo = db.Column(db.String(64))
    price = db.Column(db.Integer)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    state = db.Column(db.String(5))


items = db.relationship('OrderItem', backref='order', lazy='dynamic')  #


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fruit_id = db.Column(db.Integer)
    num = db.Column(db.Integer)
