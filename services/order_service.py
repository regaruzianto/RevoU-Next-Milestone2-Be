from model.orderModel import Order, OrderItem
from model.cartModel import CartItem
from model.productModel import Product
from connector.db import db
from schemas.order_schema import OrderSchema, OrderCreateSchema
from marshmallow import ValidationError
from sqlalchemy import desc

class OrderService:
    @staticmethod
    def get_orders(user_id, page=1, per_page=10):
        try:
            # Get paginated orders for user
            pagination = Order.query.filter_by(user_id=user_id)\
                .order_by(desc(Order.created_at))\
                .paginate(page=page, per_page=per_page)
            
            schema = OrderSchema(many=True)
            return {
                'status': 'success',
                'message': 'Order berhasil diambil',
                'data': schema.dump(pagination.items),
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
                'message': 'Terjadi kesalahan saat mengambil order',
                'errors': str(e)
            }

    @staticmethod
    def get_order_by_id(user_id, order_id):
        try:
            # Get specific order for user
            order = Order.query.filter_by(
                order_id=order_id,
                user_id=user_id
            ).first()
            
            if not order:
                return {
                    'status': 'error',
                    'message': 'Order tidak ditemukan'
                }
            
            schema = OrderSchema()
            return {
                'status': 'success',
                'message': 'Order berhasil diambil',
                'data': schema.dump(order)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat mengambil order',
                'errors': str(e)
            }

    @staticmethod
    def create_order(user_id, data):
        try:
            # Start database transaction
            with db.session.begin():
            
                # Validate shipping data
                schema = OrderCreateSchema()
                data = schema.load(data)

                # Get cart items with explicit locking
                cart_items = CartItem.query.filter_by(user_id=user_id).with_for_update().all()

                if not cart_items:
                    return {
                        'status': 'error',
                        'message': 'Cart kosong'
                    }
            
                # Calculate total amount and validate stock
                total_amount = 0
                order_items = []

                for cart_item in cart_items:
                    product = cart_item.product

                    # Validate product availability and stock
                    if not product or product.status != 'active':
                        return {
                            'status': 'error',
                            'message': f'Produk {product.name} tidak tersedia'
                        }

                    if product.stock < cart_item.quantity:
                        return {
                            'status': 'error',
                            'message': f'Stok {product.name} tidak mencukupi'
                        }

                    # Calculate item total
                    item_total = product.price * cart_item.quantity
                    total_amount += item_total

                    # Prepare order item
                    order_items.append({
                        'product_id': product.product_id,
                        'quantity': cart_item.quantity,
                        'price': product.price
                    })

                    # Update product stock
                    product.stock -= cart_item.quantity
            
                # Create order
                order = Order(
                    user_id=user_id,
                    total_amount=total_amount,
                    shipping_address=data['shipping_address'],
                    shipping_city=data['shipping_city'],
                    shipping_postal_code=data['shipping_postal_code']
                )
                db.session.add(order)
                db.session.flush()  # Get order ID

                # Create order items
                for item_data in order_items:
                    order_item = OrderItem(
                        order_id=order.order_id,
                        product_id=item_data['product_id'],
                        quantity=item_data['quantity'],
                        price=item_data['price']
                    )
                    db.session.add(order_item)

                # Clear cart
                CartItem.query.filter_by(user_id=user_id).delete()
        
            
            # Return created order
            schema = OrderSchema()
            return {
                'status': 'success',
                'message': 'Order berhasil dibuat',
                'data': schema.dump(order)
            }
            
        except ValidationError as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': 'Validasi gagal',
                'errors': e.messages
            }
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat membuat order',
                'errors': str(e)
            }

    @staticmethod
    def cancel_order(user_id, order_id):
        try:
            with db.session.begin():
                # Get order
                order = Order.query.filter_by(
                    id=order_id,
                    user_id=user_id
                ).with_for_update().first()

                if not order:
                    return {
                        'status': 'error',
                        'message': 'Order tidak ditemukan'
                    }

                # Only allow cancellation of pending orders
                if order.status != 'pending':
                    return {
                        'status': 'error',
                        'message': 'Order tidak dapat dibatalkan'
                    }

                # Start transaction
                db.session.begin_nested()

                # Return stock
                for item in order.items:
                    product = Product.query.get(item.product_id)
                    if product:
                        product.stock += item.quantity

                # Update order status
                order.status = 'cancelled'
            
            
            return {
                'status': 'success',
                'message': 'Order berhasil dibatalkan'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat membatalkan order',
                'errors': str(e)
            } 