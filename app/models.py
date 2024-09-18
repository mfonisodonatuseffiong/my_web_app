from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from app import db, bcrypt
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Admin status
    orders = db.relationship('Order', backref='user', lazy=True)  # Relationship to orders
    cart = db.relationship('Cart', uselist=False, backref='user', lazy=True)  # One-to-one relationship with cart

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def set_password(self, password):
        """Set the user's password with hashing."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)  # Relationship to order items
    cart_items = db.relationship('CartItem', backref='product', lazy=True)  # Relationship to cart items

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)  # Relationship to products

    def __repr__(self):
        return f"Category('{self.name}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    items = db.relationship('OrderItem', backref='order', lazy=True)  # Relationship to order items

    def __repr__(self):
        return f"Order('{self.id}', '{self.user_id}', '{self.status}', '{self.order_date}')"

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"OrderItem('{self.id}', '{self.product_id}', '{self.quantity}')"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)  # Relationship to cart items

    def __repr__(self):
        return f"Cart('{self.id}', '{self.user_id}')"

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Store product price at time of addition

    def __repr__(self):
        return f"CartItem('{self.id}', '{self.product_id}', '{self.quantity}')"

class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ContactSubmission('{self.id}', '{self.name}')"
