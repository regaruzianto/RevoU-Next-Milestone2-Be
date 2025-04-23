from imagekit_config import imagekit
from werkzeug.utils import secure_filename
import logging
import traceback
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import base64
import os


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
                    "message": "File harus berupa gambar (jpg, jpeg, png, gif)."
                }
            

            # cek ukuran file
            file.seek(0, os.SEEK_END)
            size_mb = file.tell()/ (1024 * 1024)
            file.seek(0)

            MAX_FILE_SIZE_MB = 1

            if size_mb > MAX_FILE_SIZE_MB:
                return f'File terlalu besar maksimal {MAX_FILE_SIZE_MB} MB'
            

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
         
        