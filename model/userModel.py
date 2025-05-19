from connector.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class GenderEnum(enum.Enum):
    male = 'male'
    female = 'female'


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # image url dan Id imagekit
    user_image = db.Column(db.String(255), nullable=True)
    user_imageId = db.Column(db.String(255), nullable= True)

    # Profile fields
    address_street = db.Column(db.String(255), nullable=True)
    address_city = db.Column(db.String(100), nullable=True)
    address_district = db.Column(db.String(100), nullable=True)
    address_subdistrict = db.Column(db.String(100), nullable=True)
    address_zipcode = db.Column(db.String(20), nullable=True)
    address_country = db.Column(db.String(100), nullable=True, default='Indonesia')
    phone = db.Column(db.String(20), nullable=True)
    
    # Status and timestamps
    status = db.Column(db.String(20), nullable=False, default='active')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    gender = db.Column(db.Enum(GenderEnum, name="genderenum"), nullable=True)

    # Relationships
    cart_items = db.relationship('CartItem', backref='user')
    orders = db.relationship('Order', backref='user')
    banks = db.relationship('Bank', backref = 'user')
    visitors = db.relationship('Visitor', backref = 'user', )
    # shops = db.relationship('Shop', backref='user')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'user_image': self.user_image,
            'user_imageId': self.user_imageId,
            'address_street': self.address_street,
            'address_city': self.address_city,
            'address_district': self.address_district,
            'address_subdistrict': self.address_subdistrict,
            'address_zipcode': self.address_zipcode,
            'address_country': self.address_country,
            'phone': self.phone,
            'gender': self.gender.name if self.gender else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<User {self.name}>'

    