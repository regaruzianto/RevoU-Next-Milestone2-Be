from model.productImageModel import ProductImage
from connector.db import db
from schemas.order_schema import OrderSchema, OrderCreateSchema
from marshmallow import ValidationError
from schemas.productImage_schema import ProductImageSchema

class ProductImageService:
    @staticmethod
    def get_product_images(product_id):
        try:
            product_images = ProductImage.query.filter_by(product_id=product_id).all()

            schema = ProductImageSchema(many=True)
            return {
                'status': 'success',
                'message': 'Produk berhasil diambil',
                'data': schema.dump(product_images)
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat mengambil produk',
                'errors': str(e)
            }
        
    @staticmethod
    def get_all_productImages():
        try:
            product_images = ProductImage.query.all()

            schema = ProductImageSchema(many=True)
            return {
                'status': 'success',
                'message': 'Produk berhasil diambil',
                'data': schema.dump(product_images)
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat mengambil produk',
                'errors': str(e)
            }