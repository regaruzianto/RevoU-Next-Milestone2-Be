from model.productVisitorModel import ProductVisitor
from model.userModel import User
from model.shopModel import Shop
from connector.db import db
from marshmallow import ValidationError
from sqlalchemy import desc,asc, func
from sqlalchemy.orm import joinedload
from schemas.productVisitor_schema import ProductVisitorQuerySchema, ProductVisitorSchema, ShopVisitorQuerySchema
import datetime


class ProductVisitorService():


    @staticmethod
    def get_product_visitors_daily(query_params=None):
        try:                        

            # validate and parse query parameter
            schema = ProductVisitorQuerySchema()
            params = schema.load(query_params or {})
            product_id = int(params['product_id'])
            

            if params.get('visit_date'):
                date = params['visit_date']
            else:
                date = datetime.date.today() 

            # base query
            query = ProductVisitor.query.options(joinedload(ProductVisitor.user)).join(User).filter(func.date(ProductVisitor.visit_date) == date, ProductVisitor.product_id == product_id)

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
                    query =  query.order_by(desc(ProductVisitor.visit_date))
                elif params['sort'] == 'oldest':
                    query = query.order_by(asc(ProductVisitor.visit_date))

            # apply pagination
            page = params.get('page', 1)
            per_page = params.get('per_page', 20)
            visitors = query.paginate(page=page, per_page=per_page, error_out=False)

            # serialize data
            schema = ProductVisitorSchema(many=True)
            data = schema.dump(visitors.items)

            return {
                'status': 'success',
                'message': 'Data visitor berhasil diambil',
                'data': data,
                'pagination': {
                    'page': visitors.page,
                    'per_page': visitors.per_page,
                    'total_pages': visitors.pages,
                    'total_items': visitors.total
                }
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan server',
                'error': str(e)
            }


    @staticmethod
    def track_product_visitors(user_id, product_id):
        try:

            # check visitor
            today = datetime.date.today()
            exist_visitor = ProductVisitor.query.filter(ProductVisitor.user_id == user_id, func.date(ProductVisitor.visit_date) == today, ProductVisitor.product_id == product_id).first()

            if exist_visitor:
                return {
                    'status': 'error',
                    'message': 'Visitor sudah tercatat'
                }

            visitors = ProductVisitor(user_id, product_id)
            db.session.add(visitors)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Data visitor berhasil diambil',
                'data': visitors.to_dict()
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan server',
                'error': str(e)
            }
        
    
    @staticmethod
    def get_shop_visitors(query_params=None):
        try:

            # validate and parse query parameter
            schema = ShopVisitorQuerySchema()
            params = schema.load(query_params or {})
            shop_id = int(params['shop_id'])

            if params.get('visit_date'):
                date = params['visit_date']
            else:
                date = datetime.date.today() 


            # base query
            query = ProductVisitor.query.options(joinedload(ProductVisitor.user)).join(User).filter(func.date(ProductVisitor.visit_date) == date, ProductVisitor.shop_id == shop_id)

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
                    query =  query.order_by(desc(ProductVisitor.visit_date))
                elif params['sort'] == 'oldest':
                    query = query.order_by(asc(ProductVisitor.visit_date))

            # apply pagination
            page = params.get('page', 1)
            per_page = params.get('per_page', 20)
            visitors = query.paginate(page=page, per_page=per_page, error_out=False)

            # serialize data
            schema = ProductVisitorSchema(many=True)
            data = schema.dump(visitors.items)

            return {
                'status': 'success',
                'message': 'Data shop visitor berhasil diambil',
                'data': data,
                'pagination': {
                    'page': visitors.page,
                    'per_page': visitors.per_page,
                    'total_pages': visitors.pages,
                    'total_items': visitors.total   
                }
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan server',
                'error': str(e)
            }
        
    
    @staticmethod
    def track_shop_visitors(user_id, shop_id):
        try:

            # check visitor
            today = datetime.date.today()
            exist_visitor = ProductVisitor.query.filter(ProductVisitor.user_id == user_id, func.date(ProductVisitor.visit_date) == today, ProductVisitor.shop_id == shop_id).first()

            if exist_visitor:
                return {
                    'status': 'error',
                    'message': 'Visitor sudah tercatat'
                }

            visitors = ProductVisitor(user_id, shop_id=shop_id)
            db.session.add(visitors)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Data visitor berhasil diambil',
                'data': visitors.to_dict()
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan server',
                'error': str(e)
            }