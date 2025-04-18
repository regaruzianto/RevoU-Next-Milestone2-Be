from model.cartModel import CartItem
from model.productModel import Product
from connector.db import db
from schemas.cart_schema import CartItemSchema, CartItemCreateSchema, CartItemUpdateSchema
from marshmallow import ValidationError

class CartService:
    @staticmethod
    def get_cart(user_id):
        try:
            # Get all active cart items for user
            cart_items = CartItem.query.filter_by(user_id=user_id).all()
            
            # Calculate totals
            total_items = sum(item.quantity for item in cart_items)
            total_amount = sum(item.quantity * item.product.price for item in cart_items)
            
            schema = CartItemSchema(many=True)
            return {
                'success': True,
                'message': 'Cart berhasil diambil',
                'data': schema.dump(cart_items),
                'total_items': total_items,
                'total_amount': float(total_amount)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': 'Terjadi kesalahan saat mengambil cart',
                'errors': str(e)
            }

    @staticmethod
    def add_to_cart(user_id, data):
        try:
            # Validate input data
            schema = CartItemCreateSchema()
            data = schema.load(data)
            
            # Check if product exists and has enough stock
            product = Product.query.get(data['product_id'])
            if not product or product.status != 'active':
                return {
                    'success': False,
                    'message': 'Produk tidak ditemukan'
                }
            
            if product.stock < data['quantity']:
                return {
                    'success': False,
                    'message': 'Stok produk tidak mencukupi'
                }
            
            # Check if product already in cart
            cart_item = CartItem.query.filter_by(
                user_id=user_id,
                product_id=data['product_id']
            ).first()
            
            if cart_item:
                # Update quantity if already in cart
                new_quantity = cart_item.quantity + data['quantity']
                if new_quantity > 10:
                    return {
                        'success': False,
                        'message': 'Maksimal 10 item per produk dalam cart'
                    }
                cart_item.quantity = new_quantity
            else:
                # Create new cart item
                cart_item = CartItem(
                    user_id=user_id,
                    product_id=data['product_id'],
                    quantity=data['quantity']
                )
                db.session.add(cart_item)
            
            db.session.commit()
            
            # Return updated cart
            return CartService.get_cart(user_id)
            
        except ValidationError as e:
            return {
                'success': False,
                'message': 'Validasi gagal',
                'errors': e.messages
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': 'Terjadi kesalahan saat menambah item ke cart',
                'errors': str(e)
            }

    @staticmethod
    def update_cart_item(user_id, item_id, data):
        try:
            # Validate input data
            schema = CartItemUpdateSchema()
            data = schema.load(data)
            
            # Find cart item
            cart_item = CartItem.query.filter_by(
                id=item_id,
                user_id=user_id
            ).first()
            
            if not cart_item:
                return {
                    'success': False,
                    'message': 'Item tidak ditemukan dalam cart'
                }
            
            # Check product stock
            if cart_item.product.stock < data['quantity']:
                return {
                    'success': False,
                    'message': 'Stok produk tidak mencukupi'
                }
            
            # Update quantity
            cart_item.quantity = data['quantity']
            db.session.commit()
            
            # Return updated cart
            return CartService.get_cart(user_id)
            
        except ValidationError as e:
            return {
                'success': False,
                'message': 'Validasi gagal',
                'errors': e.messages
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': 'Terjadi kesalahan saat mengupdate item cart',
                'errors': str(e)
            }

    @staticmethod
    def remove_from_cart(user_id, item_id):
        try:
            # Find and delete cart item
            cart_item = CartItem.query.filter_by(
                id=item_id,
                user_id=user_id
            ).first()
            
            if not cart_item:
                return {
                    'success': False,
                    'message': 'Item tidak ditemukan dalam cart'
                }
            
            db.session.delete(cart_item)
            db.session.commit()
            
            # Return updated cart
            return CartService.get_cart(user_id)
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': 'Terjadi kesalahan saat menghapus item dari cart',
                'errors': str(e)
            }

    @staticmethod
    def clear_cart(user_id):
        try:
            # Delete all cart items for user
            CartItem.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Cart berhasil dikosongkan'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': 'Terjadi kesalahan saat mengosongkan cart',
                'errors': str(e)
            } 