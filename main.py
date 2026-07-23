from fastapi import FastAPI
import database_models
from models import Product
from database import session, engine

app = FastAPI()

# Creating the tables
database_models.Base.metadata.create_all(bind=engine)

# Homepage route
@app.get("/")
def greet_user():
    return "Welcome to Telusko Trac"

products = [
    Product(id=1, name="Phone", description="A smartphone", price=10.99, stock=100),
    Product(id=2, name="Laptop", description="A portable computer", price=19.99, stock=50),
    Product(id=3, name="Mic", description="A microphone", price=5.99, stock=200),
    Product(id=4, name="Camera", description="A digital camera", price=15.99, stock=30),
    Product(id=5, name="Headphones", description="A pair of headphones", price=7.99, stock=80),
    Product(id=6, name="Tablet", description="A tablet device", price=12.99, stock=60),
]

# Products route
@app.get("/products")
def get_products():
    return products

# Product by ID route
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"error": "Product not found"}


# Create a new product route
@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product


# Update a product route
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for product in products:
        if product.id == product_id:
            product.name = updated_product.name
            product.description = updated_product.description
            product.price = updated_product.price
            product.stock = updated_product.stock
            return product

    return {"error": "Product not found"}


# Delete a product route
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return {"message": "Product deleted successfully"}

    return {"error": "Product not found"}


# SQLAlchemy Operations

@app.get("/products")
def get_products():

    # db connection
    db = session()

    # query the database
    db.query(Product).all()
    return products
