from app import create_app, db
from app.models import User
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    # Check if the user already exists
    existing_user = User.query.filter_by(email='kaytwobaba@gmail.com').first()

    if existing_user:
        print("Admin user already exists.")
    else:
        # Define the admin user
        admin = User(
            username='admin',
            email='kaytwobaba@gmail.com',
            password=bcrypt.generate_password_hash('effiongeffiong').decode('utf-8'),
            is_admin=True
        )
        
        # Add the admin user to the database
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
