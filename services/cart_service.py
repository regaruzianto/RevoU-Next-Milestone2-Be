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
                'status': "success",
                'message': 'Cart berhasil diambil',
                'data': schema.dump(cart_items),
                'total_items': total_items,
                'total_amount': float(total_amount)
            }
            
        except Exception as e:
            return {
                'status': "error",
                'message': 'Terjadi kesalahan saat mengambil cart',
                'errors': str(e)
            }

    @staticmethod
    def add_to_cart(user_id, data):
        try:
            # Validate input data
            schema = CartItemCreateSchema()
            data = schema.load(data)
            
            # Start transaction with explicit locking
            with db.session.begin():
            
                # Check if product exists and has enough stock
                product = Product.query.filter_by(product_id = data['product_id'], status = 'active') \
                    .with_for_update() \
                    .first()

                if not product:
                    return {
                        'status': "error",
                        'message': 'Produk tidak ditemukan'
                    }
            
                if product.stock < data['quantity']:
                    return {
                        'status': "error",
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
                            'status': "error",
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
            
            
            # Return updated cart
            return CartService.get_cart(user_id)
            
            
        except ValidationError as e:
            return {
                'status': "error",
                'message': 'Validasi gagal',
                'errors': e.messages
            }
        except Exception as e:
            db.session.rollback()
            return {
                'status': "error",
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
                cart_id=item_id,
                user_id=user_id
            ).first()
            
            if not cart_item:
                return {
                    'status': "error",
                    'message': 'Item tidak ditemukan dalam cart'
                }
            
            # Check product stock
            if cart_item.product.stock < data['quantity']:
                return {
                    'status': "error",
                    'message': 'Stok produk tidak mencukupi'
                }
            
            # Update quantity
            cart_item.quantity = data['quantity']
            db.session.commit()
            
            # Return updated cart
            return CartService.get_cart(user_id)
            
        except ValidationError as e:
            return {
                'status': "error",
                'message': 'Validasi gagal',
                'errors': e.messages
            }
        except Exception as e:
            db.session.rollback()
            return {
                'status': "error",
                'message': 'Terjadi kesalahan saat mengupdate item cart',
                'errors': str(e)
            }

    @staticmethod
    def remove_from_cart(user_id, item_id):
        try:
            # Find and delete cart item
            cart_item = CartItem.query.filter_by(
                cart_id=item_id,
                user_id=user_id
            ).first()
            
            if not cart_item:
                return {
                    'status': "error",
                    'message': 'Item tidak ditemukan dalam cart'
                }
            
            db.session.delete(cart_item)
            db.session.commit()
            
            # Return updated cart
            return CartService.get_cart(user_id)
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': "error",
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
                'status': "success",
                'message': 'Cart berhasil dikosongkan'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': "error",
                'message': 'Terjadi kesalahan saat mengosongkan cart',
                'errors': str(e)
            } 