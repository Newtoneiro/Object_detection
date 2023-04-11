from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.image import AsyncImage

from ultralytics import YOLO
import cv2

import os

DIRNAME = os.path.dirname(__file__)
CAPTURES_DIR = "captures"
PREDICTIONS_DIR = "predictions"


class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._model = YOLO("yolov8n.pt")
        self._captures_dir_path = os.path.join(DIRNAME, CAPTURES_DIR)
        self._predictions_dir_path = os.path.join(DIRNAME, PREDICTIONS_DIR)

        self.orientation = "vertical"
        self._camera = Camera(resolution=(720, 1080))
        self._camera.play = True

        self._prediction_path = os.path.join(self._predictions_dir_path,
                                             'prediction.png')
        self._prediction_image = AsyncImage(source=self._prediction_path)

        self._btn_on_off = Button(text="On/Off")
        self._btn_on_off.bind(on_press=self.handle_btn_on_off_press)

        self._btn_on_off.size_hint = (1, 0.2)

        self._camera_layout = BoxLayout(orientation="horizontal")
        self._camera_layout.add_widget(self._camera)
        self._camera_layout.add_widget(self._prediction_image)

        self.add_widget(self._camera_layout)
        self.add_widget(self._btn_on_off)

    def handle_btn_on_off_press(self, instance):
        capture_path = os.path.join(self._captures_dir_path, "capture.png")
        prediction_path = os.path.join(self._predictions_dir_path,
                                       "prediction.png")
        self._camera.export_to_png(capture_path)
        prediction = self._model(capture_path)
        cv2.imwrite(prediction_path, prediction[0].plot())
        self._prediction_image.reload()


class ImageDetectionApp(App):
    pass


if __name__ == '__main__':
    ImageDetectionApp().run()
