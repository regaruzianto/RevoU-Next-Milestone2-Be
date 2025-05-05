from flask import Flask, jsonify
from flask_cors import CORS
from connector.db import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from router.userRoute import user_bp
from router.productRoute import product_bp
from router.orderRoute import order_bp
from router.cartRoute import cart_bp
from router.uploadRoute import upload_bp
from router.bankRoute import bank_bp
from router.productImageRoute import productImage_bp
from router.visitorRoute import visitor_bp
from imagekitio import ImageKit
# from celery_app import celery
import os


# Inisialisasi app
app = Flask(__name__)
CORS(app) # Ijinkan CORS
jwt = JWTManager(app) # Aktifkan JWT


# # konfigurasi Celery
# app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
# app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_BROKER_URL')
# celery.conf.update(app.config)

# konfigurasi JWT 
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')  


# Konfigurasi Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_CONNECTION_STRING')
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise RuntimeError("Environment Variable 'POSTGRES_CONNECTION_STRING' is not set!")

print(f"DATABASE URI : {app.config['SQLALCHEMY_DATABASE_URI']}")
print(os.getenv('POSTGRES_CONNECTION_STRING'))


# Inisiasi Database dan migrasi
db.init_app(app)
migrate = Migrate(app,db)


# register blueprint route
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(upload_bp, url_prefix='/upload')
app.register_blueprint(bank_bp, url_prefix='/bank')
app.register_blueprint(productImage_bp, url_prefix='/productImage')
app.register_blueprint(visitor_bp, url_prefix='/visitor')

# global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    print("DEBUG ERROR:")
    traceback.print_exc()
    return jsonify({
        "status": "error",
        "message": "Terjadi kesalahan pada server",
        "error": str(e)
    }), 500


# rute root
@app.route("/")
def index():
    return jsonify({
        "status" : "success",
        "message": "Hello World!"
    })

if __name__ == "__main__":
    app.run(debug=True)