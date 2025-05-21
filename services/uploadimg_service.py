from imagekit_config import imagekit
from werkzeug.utils import secure_filename
import logging
import traceback
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import base64
import os
from model.userModel import User
from model.productImageModel import ProductImage
from model.shopModel import Shop
from connector.db import db


# Setup logging
logging.basicConfig(level=logging.DEBUG)

class UploadImageService:
    @staticmethod
    def upload(file, folder_name):
        try:
            # validasi file
            if not file or file.filename == '':
                return {
                    "status": "error",
                    "message": "Tidak ada file yang diupload."
                }
            
            # Validasi ekstensi file
            allowed_extensions = {'jpg', 'jpeg', 'png'}
            if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                return {
                    "status": "error",
                    "message": "File harus berupa gambar (jpg, jpeg, png)."
                }
            

            # cek ukuran file
            file.seek(0, os.SEEK_END)
            size_mb = file.tell()/ (1024 * 1024)
            file.seek(0)

            MAX_FILE_SIZE_MB = 1

            if size_mb > MAX_FILE_SIZE_MB:
                return {
                    'status': 'error',
                    'message': f'File terlalu besar maksimal {MAX_FILE_SIZE_MB} MB'
                }
            

            # Mengonversi file ke base64 untuk upload ke imagekit
            file_data = base64.b64encode(file.read()).decode('utf-8')
            base64_string = f"data:{file.content_type};base64,{file_data}"


            # Menggunakan secure_filename untuk memastikan nama file aman
            file_name = secure_filename(file.filename)


            # Membuat opsi upload dengan folder
            options = UploadFileRequestOptions(folder=folder_name)


            # Upload file ke ImageKit
            upload = imagekit.upload_file(
                file=base64_string,
                file_name=file_name,
                options=options  # Menambahkan opsi folder
            )

            logging.debug(f"Upload response: {upload}")
            logging.debug(f"Upload type: {type(upload)}")

            return {
                "status": "success",
                "message": "Gambar berhasil diupload.",
                "data": {
                    "url": upload.url,
                    "fileId": upload.file_id,
                    "name": upload.name
                }
            }

        except Exception as e:
            logging.error(f"Terjadi kesalahan pada upload image: {str(e)}")
            logging.error(traceback.format_exc())  # Untuk melacak error lebih rinci
            return {
                "status": "error",
                "message": "Terjadi kesalahan pada upload image.",
                "error": str(e)
            }
        
    @staticmethod
    def delete_imagekit(file_id):
        try:
            delete = imagekit.delete_file(file_id=file_id)

            return {
                "status": "success",
                "message": "Gambar berhasil dihapus.",
                "data": delete
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "Terjadi kesalahan pada delete image.",
                "error": str(e)
            }
    @staticmethod
    def upload_image_profile(file, user_id):
        try: 
            user = User.query.filter_by(user_id=user_id).first()

            if not user:
                return {
                    'status': 'error',
                    'message': 'User tidak ditemukan'
                }
            
            # Menghapus gambar lama
            if user.user_imageId:
                delete = UploadImageService.delete_imagekit(user.user_imageId)

                if delete.get('status') == 'error':
                    return delete
                

            # Upload gambar baru
            result = UploadImageService.upload(file, folder_name='/users/profile')

            user.user_image = result['data']['url']
            user.user_imageId = result['data']['fileId']

            db.session.commit()
            return {
            'status': 'success',
            'message': 'User berhasil diupdate',
            'data': user.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {
                "status": "error",
                "message": "Terjadi kesalahan pada upload image.",
                "error": str(e)
            }
        
    @staticmethod 
    def delete_image_profile(user_id):
        try:
            user = User.query.filter_by(user_id=user_id).first()

            if not user:
                return {
                    'status': 'error',
                    'message': 'User tidak ditemukan'
                }

            if user.user_imageId:
                delete = UploadImageService.delete_imagekit(user.user_imageId)

                if delete.get('status') == 'error':
                    return delete

                user.user_image = None
                user.user_imageId = None

                db.session.commit()
                return {
                'status': 'success',
                'message': 'User berhasil diupdate',
                'data': user.to_dict()
                }
            else:
                return {
                    'status': 'error',
                    'message': 'User tidak memiliki gambar profil'
                }
        except Exception as e:
            db.session.rollback()
            return {
                "status": "error",
                "message": "Terjadi kesalahan pada upload image.",
                "error": str(e)
            }
        
    @staticmethod
    def upload_product_image(product_id,file, folder_name='/products'):
        try:
            # cek jumlah image
            existing_image = ProductImage.query.filter_by(product_id=product_id).all()
            count_image = len(existing_image)
            if count_image == 3:
                return {
                    'status': 'error',
                    'message': 'Jumlah batas maksimum gambar product adalah 3',
                    'data': count_image
                }
            
            # upload dan simpan ke db
            result = UploadImageService.upload(file, folder_name=folder_name)

            if result.get('status') == 'success':
                new_image = ProductImage(
                    product_id = product_id,
                    image_url = result['data']['url'],
                    file_id = result['data']['fileId']
                )
                db.session.add(new_image)
                db.session.commit()
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": "Terjadi kesalahan pada upload image.",
                "error": str(e)
            }
      

    
    @staticmethod
    def upload_multiple_product_image(product_id,files, folder_name='/products'):
        result = []
        max_image_toupload = 3
        try:
            # cek jumlah image
            existing_image = ProductImage.query.filter_by(product_id=product_id).all()
            count_image = len(existing_image)  

            if count_image > max_image_toupload:
                return {
                    'status': 'error',
                    'message': f'jumlah gambar melebihi batas maksimum {max_image_toupload}, saat ini sudah ada {count_image} gambar',                    
                }
            

            # iterasi setiap file
            for file in files:
                # upload file
                upload = UploadImageService.upload(file=file , folder_name= folder_name)

                if upload.get('status') == 'success':
                    new_image = ProductImage(
                        product_id = product_id,
                        image_url = upload['data']['url'],
                        file_id = upload['data']['fileId']
                    )
                    # simpan ke db
                    db.session.add(new_image)
                
                result.append(upload)
            
            db.session.commit()
            return result
        
        except Exception as e:
            db.session.rollback()
            logging.error(f"Terjadi kesalahan saat upload & save images: {str(e)}")
            logging.error(traceback.format_exc())
            return result
            
    @staticmethod
    def delete_product_image(product_id, file_id):
        try:
            image = ProductImage.query.filter_by(product_id=product_id, file_id=file_id).first()

            if not image:
                return {
                    'status': 'error',
                    'message': 'Image tidak ditemukan'
                }

            delete = UploadImageService.delete_imagekit(file_id)

            if delete.get('status') == 'error':
                return delete

            db.session.delete(image)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Image berhasil dihapus'
            }
        except Exception as e:
            db.session.rollback()
            return {
                "status": "error",
                "message": "Terjadi kesalahan pada upload image.",
                "error": str(e)
            }
        
    @staticmethod
    def upload_shop_image(file, user_id):
        try:

            shop = Shop.query.filter_by(user_id=user_id).first()

            if not shop:
                return {
                    'status': 'error',
                    'message': 'Toko tidak ditemukan'
                }
            
            # cek existing image
            if shop.shop_imageId:
                delete = UploadImageService.delete_imagekit(shop.shop_imageId)

                if delete.get('status') == 'error':
                    return delete


            # Upload gambar baru
            result = UploadImageService.upload(file, folder_name='/shops/profile')

            shop.shop_image = result['data']['url']
            shop.shop_imageId = result['data']['fileId']

            db.session.commit()
            return {
            'status': 'success',
            'message': 'Gambar Toko berhasil diupdate',
            'data': shop.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {
                "status": "error",
                "message": "Terjadi kesalahan pada upload image.",
                "error": str(e)
            }
                    

