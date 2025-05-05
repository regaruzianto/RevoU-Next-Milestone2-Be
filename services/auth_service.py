from flask_jwt_extended import create_access_token
from datetime import timedelta
from model.userModel import User, GenderEnum
from connector.db import db
from schemas.auth_schema import RegisterSchema, LoginSchema, UpdateUserSchema
from marshmallow import ValidationError
from services.uploadimg_service import UploadImageService



class AuthService:
    @staticmethod
    def register(data):
        try:
            # Validate input data
            schema = RegisterSchema()
            data = schema.load(data)
            
            # Check if email already exists
            if User.query.filter_by(email=data['email']).first():
                raise ValidationError({'email': ['Email sudah terdaftar']})
            
            # Create new user
            user = User(
                name='Username',
                email=data['email'],
                password=data['password']
            )
            
            # Add optional fields if provided
            for field in ['phone', 'address_street', 'address_city', 
                         'address_district', 'address_subdistrict', 
                         'address_zipcode', 'address_country']:
                if field in data:
                    setattr(user, field, data[field])
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            # Create access token
            access_token = create_access_token(
                identity=user.user_id,
                expires_delta=timedelta(days=1)
            )
            
            return {
                'status': "success",
                'message': 'Registrasi berhasil',
                'data': {
                    'access_token': access_token,
                    'token_type': 'Bearer',
                    'user': user.to_dict()
                }
            }
            
        except ValidationError as e:
            return {
                'status': "error",
                'message': 'Validasi gagal',
                'errors': e.messages
            }
        
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat registrasi',
                'errors': str(e)
            }

    @staticmethod
    def login(data):
        try:
            # Validate input data
            schema = LoginSchema()
            data = schema.load(data)
            
            # Find user by email
            user = User.query.filter_by(email=data['email']).first()
            
            # Check if user exists and password is correct
            if not user or not user.check_password(data['password']):
                return {
                    'status': 'error',
                    'message': 'Email atau password salah'
                }
            
            # Create access token
            access_token = create_access_token(
                identity=user.user_id,
                expires_delta=timedelta(days=1)
            )
            
            return {
                'status': 'success',
                'message': 'Login berhasil',
                'data': {
                    'access_token': access_token,
                    'token_type': 'Bearer',
                    'user': user.to_dict()
                }
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
                'message': 'Terjadi kesalahan saat login',
                'errors': str(e)
            } 
        
    @staticmethod
    def get_user(user_id):
        try:
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                return {
                    'status': 'error',
                    'message': 'User tidak ditemukan'
                }
            return {
                'status': 'success',
                'message': 'User berhasil diambil',
                'data': user.to_dict()
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan di server',
                'error': str(e)
            }

    @staticmethod
    def update_user(user_id, data):
        try:
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                return {
                    'status': 'error',
                    'message': 'User tidak ditemukan'
                }
            
            # validate input data
            schema = UpdateUserSchema()
            data = schema.load(data)

            # update user
            allowed_key = [
                    "address_city", "address_district","address_subdistrict", 
                   "address_street", "address_country", "address_zipcode",
                   "email", "name", "phone"
                ]

            # Mengupdate kolom yang valid dari input data
            for k in allowed_key:
                if k in data:
                    setattr(user, k, data[k])

            # Mengupdate kolom gender jika ada dan valid
            if 'gender' in data and data['gender']:
                try:
                    user.gender = GenderEnum(data['gender'])  # Mengubah gender menjadi enum
                except ValueError:
                    return {
                        'status': 'error',
                        'message': 'Nilai gender tidak valid'
                    }

            db.session.commit()
            return {
                'status': 'success',
                'message': 'User berhasil diupdate',
                'data': user.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan saat mengupdate user',
                'errors': str(e)
            }