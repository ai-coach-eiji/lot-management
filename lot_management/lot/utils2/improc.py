import base64
import cv2
import numpy as np
from PIL import Image

def base64_to_cv(img_code):
    # 画像コードをcv2に変換
    img_raw = np.frombuffer(base64.b64decode(img_code), np.uint8)
    img = cv2.imdecode(img_raw, cv2.IMREAD_UNCHANGED)
    return img

def cv_to_base64(cv_image):
    # cv2を画像コードに変換
    image = cv2.imencode('.jpg', cv_image)[1].tostring()
    img_code = base64.b64encode(image).decode('utf-8')
    return img_code

def cv_to_pil(image):
    # cv2(NumPy)型の画像をPIL型に変換
    return Image.fromarray(image)

def pil_to_cv(img):
    # PIL型の画像をcv2(NumPy)型に変換
    return np.array(img, dtype=np.uint8) # OpenCVのデフォルト: uint8