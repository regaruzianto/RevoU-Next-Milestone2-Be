from connector.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class ProductImage(db.Model):
    __tablename__ = 'product_images'

    productImage_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    image_url = db.Column(db.String, nullable=False)
    file_id = db.Column(db.String, nullable=True)

    def __init__(self, product_id, image_url, file_id=None):
        self.product_id = product_id
        self.image_url = image_url
        self.file_id = file_id

    def to_dict(self):
        return {
            'productImage_id': self.productImage_id,
            'product_id': self.product_id,
            'image_url': self.image_url,
            'file_id': self.file_id
        }   
    
    def __repr__(self):
        return f'<ProductImage product_id={self.product_id} image_url={self.image_url}>'