import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE_MB = 1

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file(file):
    if file.filename == '':
        return 'file tidak boleh kosong'
    
    if not allowed_file(file.filename):
        return f'format file tidak diizinkan, harus {", ".join(ALLOWED_EXTENSIONS)}'
    
    # cek ukuran file
    file.seek(0, os.SEEK_END)
    size_mb = file.tell()/ (1024 * 1024)
    file.seek(0)

    if size_mb > MAX_FILE_SIZE_MB:
        return f'File terlalu besar maksimal {MAX_FILE_SIZE_MB} MB'
    
    return None