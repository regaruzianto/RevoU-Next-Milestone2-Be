from connector.db import db
from datetime import datetime


class Visitor(db.Model):
    __tablename__ = 'visitors'

    visitor_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id):
        self.user_id = user_id,
    
    def to_dict(self):

        return {
            'visitor_id': self.visitor_id,
            'user_id': self.user.to_dict() if self.user else None,
            'visit_date': self.visit_date
        }
    
    def __repr__(self):
        return '<Visitor visitor_id={self.visitor_id} user_id={self.user_id}>'
    