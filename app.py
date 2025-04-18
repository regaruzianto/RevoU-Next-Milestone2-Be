from flask import Flask, jsonify
from flask_cors import CORS
from connector.db import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os


# Inisialisasi app
app = Flask(__name__)
CORS(app) # Ijinkan CORS
jwt = JWTManager(app) # Aktifkan JWT

# konfigurasi JWT 
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')  
jwt = JWTManager(app)


# Konfigurasi Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_CONNECTION_STRING')
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise RuntimeError("Environment Variable 'POSTGRES_CONNECTION_STRING' is not set!")

print(f"DATABASE URI : {app.config['SQLALCHEMY_DATABASE_URI']}")
print(os.getenv('POSTGRES_CONNECTION_STRING'))


# Inisiasi Database dan migrasi
db.init_app(app)
migrate = Migrate(app,db)


# rute root
@app.route("/")
def index():
    return jsonify({
        "status" : "success",
        "message": "Hello World!"
    })