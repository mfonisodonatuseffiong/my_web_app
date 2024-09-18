import logging
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Order, Product, Category, ContactSubmission, OrderItem
from app.forms import LoginForm, RegistrationForm, ContactForm
from app.payment_gateway import process_payment  # Assume a payment processing module exists

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Define the 'main' Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def home():
    logger.info("Rendering home page.")
    return render_template('home.html')

@main.route('/account')
@login_required
def account():
    logger.info(f"User {current_user.id} accessed account page.")
    return render_template('account.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            logger.info(f"User ID {user.id} logged in successfully.")
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            logger.warning(f"Failed login attempt for email {form.email.data}.")
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        logger.info(f"New user with email {form.email.data} registered successfully.")
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logger.info(f"User ID {current_user.id} logged out.")
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/products')
def products():
    categories = Category.query.all()
    logger.info("Rendering products page with categories.")
    return render_template('products.html', categories=categories)

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    logger.info(f"Rendering details for product ID {product_id}.")
    return render_template('product_detail.html', product=product)

@main.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    logger.info(f"Viewing cart with total amount {total:.2f}.")
    return render_template('cart.html', cart=cart, total=total)

@main.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({'id': product.id, 'name': product.name, 'price': product.price, 'quantity': 1})
    
    session['cart'] = cart
    logger.info(f"Added product ID {product.id} to cart.")
    return redirect(url_for('main.view_cart'))

@main.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    logger.info(f"Removed product ID {product_id} from cart.")
    return redirect(url_for('main.view_cart'))

@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)

    if not cart:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('main.products'))

    if request.method == 'POST':
        order = Order(user_id=current_user.id, total=total)
        db.session.add(order)
        db.session.commit()

        for item in cart:
            order_item = OrderItem(order_id=order.id, product_id=item['id'], quantity=item['quantity'])
            db.session.add(order_item)
        db.session.commit()

        session['order_id'] = order.id
        session.pop('cart', None)
        return redirect(url_for('main.payment'))

    return render_template('checkout.html', cart=cart, total=total)

@main.route('/order_confirmation/<int:order_id>', methods=['GET'])
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)

@main.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    order_id = session.get('order_id')
    order = Order.query.get(order_id)

    if not order:
        flash('No order found. Please try again.', 'warning')
        return redirect(url_for('main.products'))

    total = order.total
    payment_result = process_payment(total)

    if payment_result['success']:
        flash(payment_result['message'], 'success')
        return redirect(url_for('main.order_confirmation', order_id=order.id))
    else:
        flash(payment_result['message'], 'danger')
        return redirect(url_for('main.payment'))

@main.route('/profile')
@login_required
def profile():
    logger.info(f"Rendering profile page for user ID {current_user.id}.")
    return render_template('profile.html', user=current_user)

@main.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    logger.info(f"Rendering orders page for user ID {current_user.id}.")
    return render_template('orders.html', orders=user_orders)

@main.route('/search')
def search():
    query = request.args.get('query', '').strip()
    if query:
        try:
            results = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
            result_count = len(results)
            logger.info(f"Search query: {query}, {result_count} results found.")
            flash(f'{result_count} results found for "{query}".', 'success')
        except Exception as e:
            logger.error(f"Error during search query: {e}")
            flash('An error occurred while processing your search.', 'danger')
            results = []
    else:
        logger.warning('No search query provided.')
        flash('No search query provided.', 'danger')
        results = []

    return render_template('search_results.html', results=results, query=query)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact_submission = ContactSubmission(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(contact_submission)
        db.session.commit()
        logger.info(f"Contact submission received from {form.name.data} ({form.email.data}): {form.message.data}")
        flash('Thank you for your message! We will get back to you shortly.', 'success')
        return redirect(url_for('main.contact'))
    
    logger.info("Rendering contact page.")
    return render_template('contact.html', form=form)

@main.route('/about')
def about():
    logger.info("Rendering about page.")
    return render_template('about.html')
