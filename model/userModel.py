from connector.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from bcrypt import hashpw,checkpw,gensalt


class User(db.Model):
    __tablename__ ="users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    address_city = db.Column(db.String(120), nullable=True)
    address_street = db.Column(db.String(120), nullable=True)
    address_ditrict = db.Column(db.String(120), nullable=True)
    address_subditrict = db.Column(db.String(120), nullable=True)
    address_zipcode = db.Column(db.String(120), nullable=True)
    address_country = db.Column(db.String(120), nullable=True)
    
    status = db.Column(db.String(20), nullable=False, server_default='active')
    user_image = db.Column(db.String(200), nullable=True)    
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())


    def __repr__(self):
        return f'<User {self.username}> {self.email} {self.user_id}'
    
    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'address_city': self.address_city,
            'address_street': self.address_street,
            'address_ditrict': self.address_ditrict,
            'address_subditrict': self.address_subditrict,
            'address_zipcode': self.address_zipcode,
            'address_country': self.address_country,
            'status': self.status,
            'user_image': self.user_image,
            'created_at': self.created_at
        }