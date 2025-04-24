from connector.db import db
from sqlalchemy import func
from datetime import datetime

class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String(100), nullable=False)
    
    # Status and timestamps
    status = db.Column(db.String(20), nullable=False, default='active')
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    cart_items = db.relationship('CartItem', backref='product')
    order_items = db.relationship('OrderItem', backref='product')
    product_images = db.relationship('ProductImage', backref='product')

    def __init__(self, name, price, category, description=None, stock=0):
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.stock = stock

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock': self.stock,
            'category': self.category,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Product {self.name}>' 