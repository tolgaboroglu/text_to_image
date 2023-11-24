from urllib.parse import urlparse
import base64
import cv2
import numpy as np
class Utils:

    @classmethod
    def is_url(cls,url_string):
        try:
            result = urlparse(url_string)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
        
    @classmethod
    def process_local_image(cls,image_path):

        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string



    
    @classmethod
    def byte_to_image(cls,byte_array):
        nparr = np.frombuffer(byte_array, np.uint8)
        
        # Decode the numpy array to an image
        return  cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    
    @classmethod
    def convert_to_b64(cls, image):
        return base64.b64encode(image)