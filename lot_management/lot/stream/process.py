import cv2

class Stream(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if success:
            image = cv2.flip(image, 1) # webcam needs flip
            byte_image = cv2.imencode('.jpg', image)[1].tobytes()
            return byte_image

def gen(camera):
    while True:
        response = camera.get_frame()
        # フレーム画像のバイナリデータをユーザーに送付する
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + response + b'\r\n\r\n')