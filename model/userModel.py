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


    def __repr__(self):
        return f'<User {self.username}> {self.email} {self.user_id}'