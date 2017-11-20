from flask import Flask
from hashlib import md5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dreamteam@gameservers.go.ro/qa_course'
# application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1/qa_course'
application.secret_key = 'FEF9B%399-!8EF6- 4B16-[9BD4-092B1<85D632D'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)
login_manager = LoginManager()


def generate_hash(password):
    return md5((md5(application.secret_key.encode("utf-8")).hexdigest() + md5(password.encode("utf-8")).hexdigest()).encode("utf-8")).hexdigest()


def check_hash(password, stored_hash):
    return password == stored_hash


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False)
    last_name = db.Column(db.String(30), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.Text, unique=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_hash(password)

    def __repr__(self):
        return '<User: {}>'.format(self.last_name)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id


class Product(db.Model):
    """
    Create a products table
    """

    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(60), unique=True)
    product_description = db.Column(db.Text)
    product_price = db.Column(db.Float)
    tags = db.Column(db.Text)
    product_image = db.Column(db.String(30))

    def __repr__(self):
        return '<Product: {}>'.format(self.product_name)


class Cart(db.Model):
    """
    Create a cart table
    """

    __tablename__ = 'cart'

    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    quantity = db.Column(db.Integer)

    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return '<Cart: {}>'.format(self.cart_id)


class Review(db.Model):
    """
    Create a products table
    """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    product_id = db.Column(db.Integer)
    stars = db.Column(db.Integer)
    review = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def __init__(self, user_id, product_id, stars, review):
        self.user_id = user_id
        self.product_id = product_id
        self.stars = stars
        self.review = review

    def __repr__(self):
        return '<Review: {}>'.format(self.review)

db.create_all()
login_manager.init_app(application)