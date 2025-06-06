import cv2
import numpy as np
from picamera2 import Picamera2
import time

class Camera:
    def __init__(self, resolution=(1280, 720), format='RGB888'):
        self.camera = Picamera2()
        config = self.camera.create_preview_configuration(main={"size": resolution, "format": format})
        self.camera.configure(config)
        self.camera.start()
        time.sleep(2)

    def stream(self):
        try:
            while True:
                frame_array = self.camera.capture_array()
                frame_array = cv2.rotate(frame_array, cv2.ROTATE_180)
                ret, jpeg = cv2.imencode('.jpg', frame_array)
                if not ret:
                    continue
                frame = jpeg.tobytes()
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
                )
        except Exception as e:
            print(f"Erro no stream da camera: {e}")
