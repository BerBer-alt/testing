from qbay import app
from datetime import date
from flask_sqlalchemy import SQLAlchemy


'''
This file defines data models and related business logics
'''


db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(
        db.String(80), nullable=False)
    email = db.Column(
        db.String(120), unique=True, nullable=False,
        primary_key=True)
    password = db.Column(
        db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# the class for product objects
class Product(db.Model):
    product_id = db.Column(
        db.Integer, primary_key=True)
    product_title = db.Column(
        db.String(80), unique=False, nullable=False)
    product_description = db.Column(
        db.String(2000), unique=False, nullable=True)
    product_price = db.Column(
        db.Integer, nullable=False)
    last_modified_date = db.Column(
        db.Integer, unique=False, nullable=False)
    owener_email = db.Column(
        db.String(120), unique=True, nullable=False,
        primary_key=True)

    def __repr__(self):
        return "<Product %r>" % self.product_title

# create all tables
db.create_all()

def register(name, email, password):
    '''
    Register a new user
      Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password
      Returns:
        True if registration succeeded otherwise False
    '''
    # check if the email has been used:
    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False

    # create a new user
    user = User(username=name, email=email, password=password)
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return True


def login(email, password):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        The user object if login succeeded otherwise None
    '''
    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]

def update_profile(name, shipping_address, postal_code):
    '''
    Update user profile
      Parameters:
        name (string):              user name
        shipping_address (string):  shipping address
        postal_code (string):       postal code
      Returns:
        Boolean value, true for successful update otherwise update fails
    '''
    if (not(shipping_address) or (shipping_address.isalnum()==False)): return False
    if not (postal_code[0].isalpha() and postal_code[1].isnum() 
        and postal_code[2].isalpha() and postal_code[3]==" "
        and postal_code[4].isnum() and postal_code[5].isalpha()
        and postal_code[6].isnum()): return False
    if (not(name) or len(name)>=20 or len(name)<=2 
        or name[0]==" " or name[0]==" " 
        or not(all(i.isalnum() or i.isspace() for i in name))):return False
    return True

def update_product(id, title, description, price):
    # determine wheather new price is incremental than previous one
    if ( price < Product.product_price): return False
    # express last modified date in format of dd/mm/yy
    Product.last_modified_date = date.today().strftime("%d/%m/%Y")
    Product.product_id = id
    Product.product_title = title
    Product.product_description = description

