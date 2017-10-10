from flask import Flask
from hashlib import md5
from flask_sqlalchemy import SQLAlchemy
# from flaskext.mysql import MySQL

application = Flask(__name__)
# mysql = MySQL()

# MySQL configurations
# application.config['MYSQL_DATABASE_USER'] = 'root'
# application.config['MYSQL_DATABASE_PASSWORD'] = 'compas10'
# application.config['MYSQL_DATABASE_DB'] = 'qa_course'
# application.config['MYSQL_DATABASE_HOST'] = '54.244.61.130'

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:compas10@54.244.61.130/qa_course'
application.secret_key = 'FEF9B%399-!8EF6- 4B16-[9BD4-092B1<85D632D'
# mysql.init_app(application)
db = SQLAlchemy(application)
# db.create_all()


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
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_hash(password)

    def __repr__(self):
        return '<User: {}>'.format(self.last_name)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_hash(self.password, password)


class Product(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(60), unique=True)
    product_description = db.Column(db.Text)
    product_price = db.Column(db.Integer)

    def __repr__(self):
        return '<Product: {}>'.format(self.product_name)


class Cart(db.Model):
    """
    Create a Role table
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
        return '<Cart: {}>'.format(self.name)