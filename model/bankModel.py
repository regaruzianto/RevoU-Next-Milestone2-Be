from connector.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Bank(db.Model):
    __tablename__ = 'banks'

    account_id = db.Column(db.Integer, primary_key =True, nullable = False, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable= False)
    account_name = db.Column(db.String(100), nullable = False)
    account_number = db.Column(db.Integer, nullable=False, unique=True)
    code = db.Column(db.String, nullable = False )

    def __init__(self,user_id, name, number, code):
        self.user_id = user_id
        self.account_name = name
        self.account_number = number 
        self.code = code


    def __repr__(self):
        return f'<account_id = {self.account_id}, user_id ={self.user_id}, account_name = {self.account_name}, account_number = {self.account_number}, code = {self.code}>'
    
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'user_id': self.user_id,
            'account_name': self.account_name,
            'account_number': self.account_number,
            'code': self.code
        }


