from fastapi import FastAPI, Depends
# from fastapi.params import Depends
import database_models
from models import Product
from database import session, engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)

# Creating the tables
database_models.Base.metadata.create_all(bind=engine)

# Homepage route
@app.get("/")
def greet_user():
    return "Welcome to Telusko Trac"

products = [
    Product(id=1, name="Phone", description="A smartphone", price=10.99, quantity=100),
    Product(id=2, name="Laptop", description="A portable computer", price=19.99, quantity=50),
    Product(id=3, name="Mic", description="A microphone", price=5.99, quantity=200),
    Product(id=4, name="Camera", description="A digital camera", price=15.99, quantity=30),
    Product(id=5, name="Headphones", description="A pair of headphones", price=7.99, quantity=80),
    Product(id=6, name="Tablet", description="A tablet device", price=12.99, quantity=60),
]

# Dependency injection
def get_dp():
    db = session()
    try:
        yield db
    finally:
        db.close()


# Function to populate the products table
def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            db_product = database_models.Product(**product.model_dump())
            db.add(db_product)
        db.commit()
        db.close()

init_db()


# Products route
# @app.get("/products")
# def get_products():
#     return products

# Product by ID route
# @app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"error": "Product not found"}


# Create a new product route
# @app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product


# Update a product route
# @app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for product in products:
        if product.id == product_id:
            product.name = updated_product.name
            product.description = updated_product.description
            product.price = updated_product.price
            product.quantity = updated_product.quantity
            return product

    return {"error": "Product not found"}


# Delete a product route
# @app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return {"message": "Product deleted successfully"}

    return {"error": "Product not found"}


# ------------------------ CRUD OPERATIONS WITH SQLAlchemy ------------------------

# Get all products route
@app.get("/products")
def get_all_products(db: Session = Depends(get_dp)):
    db_products = db.query(database_models.Product).all()
    return db_products


# Get product by ID route
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_dp)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        return db_product
    return {"error": "Product not found"}


# Update product route
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product, db: Session = Depends(get_dp)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.quantity = updated_product.quantity
        db.commit()
        return {"product updated succesfully"}
    return {"error": "Product not found"}


# Post product route
@app.post("/products")
def create_product(product: Product, db: Session = Depends(get_dp)):
    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"Product created successfully": db_product}


# Delete product route
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_dp)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    return {"error": "Product not found"}