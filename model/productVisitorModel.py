from connector.db import db
from datetime import datetime


class ProductVisitor(db.Model):
    __tablename__ = 'product_visitors'

    product_visitor_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), nullable=True)
    visit_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, product_id = None, shop_id = None):
        self.user_id = user_id,
        self.product_id = product_id
        self.shop_id = shop_id
    
    def to_dict(self):

        return {
            'product_visitor_id': self.product_visitor_id,
            'user_id': self.user.to_dict() if self.user else None,
            'visit_date': self.visit_date
        }
    
    def __repr__(self):
        return '<Visitor visitor_id={self.visitor_id} user_id={self.user_id}>'