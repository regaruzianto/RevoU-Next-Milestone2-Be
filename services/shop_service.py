from model.shopModel import Shop
from connector.db import db
from schemas.shop_schema import ShopCreateSchema, ShopUpdateSchema
from marshmallow import ValidationError


class ShopService:
    
    @staticmethod
    def get_all_shops():
        try:
            shops = Shop.query.all()    

            return {
                'status': 'success',
                'message': 'Semua toko berhasil diambil',
                'data': [shop.to_dict() for shop in shops]
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan server',
                'error': str(e)
            }
    

    @staticmethod
    def get_shop_by_id(shop_id):
        try:
            shop = Shop.query.filter_by(shop_id=shop_id).first()

            return {
                'status': 'success',
                'message': 'Toko berhasil diambil',
                'data': shop.to_dict()
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan server',
                'error': str(e)
            }
    
    @staticmethod
    def get_shop_by_name(shop_name):
        try:
            shop_name = shop_name.lower()
            shop = Shop.query.filter_by(shop_name=shop_name).first()
            if not shop:
                return {
                    'status': 'error',
                    'message': f'Toko dengan nama "{shop_name}" tidak ditemukan'
                }

            return {
                'status': 'success',
                'message': 'Toko berhasil diambil',
                'data': shop.to_dict()
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan server',
                'error': str(e)
            }
    
    @staticmethod
    def create_shop(user_id,data):
        try:
            # Validate input data
            schema = ShopCreateSchema()
            data = schema.load(data)
            user_id = int(user_id)
            # Create new shop
            shop = Shop(
                user_id= user_id,
                shop_name=data['shop_name'].lower(),
                shop_address_city=data.get('shop_address_city').lower(),
                shop_phone=data.get('shop_phone'),
                description=data.get('description'),               
            )
            db.session.add(shop)
            db.session.commit()

            return {
                'status': 'success',
                'message': 'Toko berhasil dibuat',
                'data': shop.to_dict()
            }
        except ValidationError as e:
            return {
                'status': 'error',
                'message': 'Validasi gagal',
                'errors': e.messages
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan server',
                'error': str(e)
            }
    
    @staticmethod
    def update_shop(user_id, data):
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
            schema = ShopUpdateSchema()
            data = schema.load(data)

            # Field yang tidak perlu diubah ke lowercase
            EXCLUDED_LOWERCASE_FIELDS = ['description']

            # Ubah value menjadi lowercase jika bertipe string dan tidak masuk pengecualian
            for key in data:
                if key not in EXCLUDED_LOWERCASE_FIELDS and isinstance(data[key], str):
                    data[key] = data[key].lower()

            for key, value in data.items():
                setattr(shop, key, value)

            db.session.commit()

            return {
                'status': 'success',
                'message': 'Toko berhasil diupdate',
                'data': shop.to_dict()
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan server',
                'error': str(e)
            }
        
