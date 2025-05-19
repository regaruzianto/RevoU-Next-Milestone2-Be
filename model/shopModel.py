from connector.db import db
from datetime import datetime



class Shop(db.Model):
    __tablename__ = "shops"
    
    shop_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    shop_name = db.Column(db.String(100), nullable=False)
    shop_address_city = db.Column(db.String(255), nullable=True)
    shop_phone = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # image url dan id imagekit
    shop_image = db.Column(db.String(255), nullable=True)
    shop_imageId = db.Column(db.String(255), nullable=True)
    
    # status and timestamp
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='active')
    
    
    def __init__(self, user_id, shop_name, shop_address_city=None, shop_phone=None, description=None):
        self.user_id = user_id
        self.shop_name = shop_name

        self.shop_address_city = shop_address_city
        self.shop_phone = shop_phone
        self.description = description


    def to_dict(self):
        return {
            'shop_id': self.shop_id,
            'user_id': self.user_id,
            'shop_name': self.shop_name,
            'shop_address_city': self.shop_address_city,
            'shop_phone': self.shop_phone,
            'description': self.description,
            'shop_image': self.shop_image,
            'shop_imageId': self.shop_imageId,
            'created_at': self.created_at,
            'status': self.status
        }