import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.camera import Camera
import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import numpy as np

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()

        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

class MainApp(App):
    def build(self):
        self.capture = cv2.VideoCapture("rtsp://admin:admin1234@192.168,1,15:554/cam/realmonitor?channel=1&subtype=0")
        self.camera = KivyCamera(capture=self.capture, fps=30)
        return self.camera

if __name__== "__main__":
    MainApp().run()
