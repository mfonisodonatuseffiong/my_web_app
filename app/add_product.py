from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    # Create a new product instance
    watch = Product(
        name='Watch',
        description='A stylish wrist watch with a leather band.',
        price=650.66
    )
    
    # Add and commit the product to the database
    db.session.add(watch)
    db.session.commit()
    
    print("Product added successfully.")
