from model.productModel import Product
from connector.db import db
from schemas.product_schema import ProductSchema, ProductQuerySchema,ProductUserQuerySchema
from marshmallow import ValidationError
from sqlalchemy import desc, asc
from sqlalchemy.orm import joinedload
from model.shopModel import Shop



class ProductService:
    @staticmethod
    def get_products(query_params=None):
        try:
            # Validate and parse query parameters
            schema = ProductQuerySchema()
            params = schema.load(query_params or {})
            
            # Start with base query

            query = Product.query.filter_by(status='active')
            
            # Apply filters
            if params.get('shop_id'):
                query = query.filter(Product.shop_id == params['shop_id'])
            if params.get('category'):
                query = query.filter_by(category=params['category'])
            if params.get('min_price'):
                query = query.filter(Product.price >= params['min_price'])
            if params.get('max_price'):
                query = query.filter(Product.price <= params['max_price'])
            
                
            # Apply sorting
            if params.get('sort'):
                if params['sort'] == 'price_asc':
                    query = query.order_by(asc(Product.price))
                elif params['sort'] == 'price_desc':
                    query = query.order_by(desc(Product.price))
                elif params['sort'] == 'newest':
                    query = query.order_by(desc(Product.created_at))
                elif params['sort'] == 'oldest':
                    query = query.order_by(asc(Product.created_at))
            
            # Apply pagination
            page = params.get('page', 1)
            per_page = params.get('per_page', 20)
            pagination = query.paginate(page=page, per_page=per_page)
            
            # Prepare response
            schema = ProductSchema(many=True)
            return {
                'status': 'success',
                'message': 'Produk berhasil diambil',
                'data': schema.dump(pagination.items),
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total_pages': pagination.pages,
                    'total_items': pagination.total
                }
            }
            
        except ValidationError as e:
            return {
                'status': 'error',
                'message': 'Parameter query tidak valid',
                'errors': e.messages
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat mengambil produk',
                'errors': str(e)
            }

    @staticmethod
    def get_product_by_id(product_id):
        try:
            product = Product.query.get(product_id)

            # product = Product.query.options(joinedload(Product.product_images)).filter(
            #     Product.product_id == product_id,
            #     Product.status == 'active'
            # ).first()
            
            
            if not product or product.status != 'active':
                return {
                    'status': 'error',
                    'message': 'Produk tidak ditemukan'
                }
            
            schema = ProductSchema()
            return {
                'status': 'success',
                'message': 'Produk berhasil diambil',
                'data': schema.dump(product)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat mengambil produk',
                'errors': str(e)
            }

    @staticmethod
    def create_product(user_id,data):
        try:
            user_id = int(user_id)
            # Find shop
            shop = Shop.query.filter_by(user_id=user_id).first()

            if not shop:
                return {
                    'status': 'error',
                    'message': 'Toko tidak ditemukan'
                }

            # Validate input data
            schema = ProductSchema()
            data = schema.load(data)
            
            # Create new product
            product = Product(
                name=data['name'],
                description=data['description'],
                category=data['category'],
                price=data['price'],
                stock=data['stock'],
                shop_id=shop.shop_id
            )
            
            # Save to database
            db.session.add(product)
            db.session.commit()
            
            return {
                'status': 'success',
                'message': 'Produk berhasil dibuat',
                'data': schema.dump(product)
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
                'message': 'Terjadi kesalahan saat membuat produk',
                'errors': str(e)
            }

    @staticmethod
    def update_product(user_id,product_id, data):
        try:
            # Find shop
            shop = Shop.query.filter_by(user_id=user_id).first()

            if not shop:
                return {
                    'status': 'error',
                    'message': 'Toko tidak ditemukan'
                }

            # Find product
            product = Product.query.filter_by(shop_id=shop.shop_id, product_id=product_id).first()
            
            if not product:
                return {
                    'status': 'error',
                    'message': 'Produk tidak ditemukan'
                }
            
            # Validate input data
            schema = ProductSchema(partial=True)
            data = schema.load(data)
            
            # Update product fields
            for key, value in data.items():
                setattr(product, key, value)
            
            # Save to database
            db.session.commit()
            
            return {
                'status': 'success',
                'message': 'Produk berhasil diupdate',
                'data': schema.dump(product)
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
                'message': 'Terjadi kesalahan saat mengupdate produk',
                'errors': str(e)
            }

    @staticmethod
    def delete_product(user_id,product_id):
        try:
            
            user_id = int(user_id)
            # check user and shop
            shop = Shop.query.filter_by(user_id=user_id).first()    

            if not shop:
                return {
                    'status': 'error',
                    'message': 'Toko tidak ditemukan'
                }

            product = Product.query.filter(Product.shop_id == shop.shop_id, Product.product_id == product_id).first()

            if not product:
                return {
                    'status': 'error',
                    'message': 'Produk tidak ditemukan'
                }
            
            if not product:
                return {
                    'status': 'error',
                    'message': 'Produk tidak ditemukan'
                }
            
            # Soft delete by updating status
            product.status = 'deleted'
            db.session.commit()
            
            return {
                'status': 'success',
                'message': 'Produk berhasil dihapus'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat menghapus produk',
                'errors': str(e)
            } 
    
    @staticmethod
    def get_products_by_userID(query_params=None):
        try:
            # Validate and parse query parameters
            schema = ProductUserQuerySchema()
            params = schema.load(query_params or {})
            user_id = int(params.get('user_id'))

            # shop
            shop = Shop.query.filter(Shop.user_id==user_id).first()

            if not shop:
                return {
                    'status': 'error',
                    'message': 'Toko tidak ditemukan'
                }


            # Start with base query

            query = Product.query.filter(Product.status=='active', Product.shop_id==shop.shop_id)
            
            # Apply filters
            if params.get('category'):
                query = query.filter_by(category=params['category'])
            if params.get('min_price'):
                query = query.filter(Product.price >= params['min_price'])
            if params.get('max_price'):
                query = query.filter(Product.price <= params['max_price'])
            
                
            # Apply sorting
            if params.get('sort'):
                if params['sort'] == 'price_asc':
                    query = query.order_by(asc(Product.price))
                elif params['sort'] == 'price_desc':
                    query = query.order_by(desc(Product.price))
                elif params['sort'] == 'newest':
                    query = query.order_by(desc(Product.created_at))
                elif params['sort'] == 'oldest':
                    query = query.order_by(asc(Product.created_at))
            
            # Apply pagination
            page = params.get('page', 1)
            per_page = params.get('per_page', 20)
            pagination = query.paginate(page=page, per_page=per_page)
            
            # Prepare response
            schema = ProductSchema(many=True)
            return {
                'status': 'success',
                'message': 'Produk berhasil diambil',
                'data': schema.dump(pagination.items),
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total_pages': pagination.pages,
                    'total_items': pagination.total
                }
            }
            
        except ValidationError as e:
            return {
                'status': 'error',
                'message': 'Parameter query tidak valid',
                'errors': e.messages
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat mengambil produk',
                'errors': str(e)
            }
