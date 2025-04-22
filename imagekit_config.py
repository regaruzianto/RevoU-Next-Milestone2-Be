from imagekitio import ImageKit
import os


imagekit = ImageKit(
    private_key = os.getenv('IMAGEKIT_PRIVATE_KEY'),
    public_key= os.getenv('IMAGEKIT_PUBLIC_KEY'),
    url_endpoint= os.getenv('IMAGEKIT_URL_ENDPOINT')
)