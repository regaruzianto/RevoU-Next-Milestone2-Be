from model.visitorModel import Visitor
from model.userModel import User
from connector.db import db
from marshmallow import ValidationError
from schemas.visitor_schema import VisitorSchema, UserVisitorQuerySchema
from sqlalchemy import desc,asc, func
from sqlalchemy.orm import joinedload
import datetime



class VisitorService:
    @staticmethod
    def get_visitors_daily(query_params=None):
        try:
            # validate and parse query parameters
            schema = UserVisitorQuerySchema()
            params = schema.load(query_params or {})
            
            if params.get('visit_date'):
                date = params['visit_date']
            else:
                date = datetime.date.today() 
                
            # base query
            query = Visitor.query.options(joinedload(Visitor.user)).join(User).filter(func.date(Visitor.visit_date) == date)

            # apply filter
            if params.get('address_city'):
                query = query.filter(User.address_city == params['address_city'])
            if params.get('address_country'):
                query = query.filter(User.address_country == params['address_country'])
            if params.get('gender'):
                query = query.filter(User.gender == params['gender'])
            
            # apply sort
            if params.get('sort'):
                if params['sort'] == 'newest':
                    query =  query.order_by(desc(Visitor.visit_date))
                elif params['sort'] == 'oldest':
                    query = query.order_by(asc(Visitor.visit_date))

            # apply pagination
            page = params.get('page', 1)
            per_page = params.get('per_page', 10)
            pagination = query.paginate(page=page, per_page=per_page)

            # serialize data
            visitor_schema = VisitorSchema(many=True)
            visitor_list = visitor_schema.dump(pagination.items)

            return {
                'status': 'success',
                'message': 'Data berhasil diambil',
                'data': visitor_list,
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total_pages': pagination.pages,
                    'total_items': pagination.total
                }
            }

            
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat mengambil data',
                'error': str(e)
            }
        
    @staticmethod
    def track_visitor(user_id):
        try:
            # check visitor
            today = datetime.date.today()
            exist_visitor = Visitor.query.filter(Visitor.user_id == user_id, func.date(Visitor.visit_date) == today).first()

            if exist_visitor:
                return {
                    'status': 'error',
                    'message': 'Visitor sudah tercatat'
                }

            visitor = Visitor(user_id=user_id)
            db.session.add(visitor)
            db.session.commit()

            schema = VisitorSchema()
            visitor = schema.dump(visitor)
            return {
                'status': 'success',
                'message': 'Visitor berhasil ditambahkan',
                'data': visitor
            }
        except ValidationError as e:
            return {
                'status': 'error',
                'message': 'Validasi gagal',
                'errors': e.messages
            }
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat menambahkan visitor',
                'errors': str(e)
            }
        
    @staticmethod 
    def count_visitor(query_params=None):
        try:
            schema = UserVisitorQuerySchema()
            params = schema.load(query_params or {})
            
            if params.get('visit_date'):
                date = params['visit_date']
            else:
                date = datetime.date.today()

            count = Visitor.query.join(User).filter(func.date(Visitor.visit_date) == date)

            if params.get('address_city'):
                count = count.filter(User.address_city == params['address_city'])
            if params.get('address_country'):
                count = count.filter(User.address_country == params['address_country'])
            if params.get('gender'):
                count = count.filter(User.gender == params['gender'])

            count = count.count()

            return {
                'status': 'success',
                'message': 'Visitor berhasil dihitung',
                'data': {
                    'tanggal': date,
                    'jumlah pengunjung': count
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat menghitung visitor',
                'errors': str(e)
            }