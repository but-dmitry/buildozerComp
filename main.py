import threading
from array import array

import kivy

from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Ellipse, Line, Rotate
from kivy.core.image import Texture
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

import pickle
import numpy as np
import struct ## new
import cv2
from kivy.clock import Clock
import socket

from PIL import Image as IMG
import PIL

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.134', 8485))
connection = client_socket.makefile('wb')

data = b""
payload_size = struct.calcsize(">L")
a = False
class Container(BoxLayout):
    def watch(self):
        Clock.schedule_interval(self.update, 0.001)

    def update(self, *args):
        global client_socket
        global payload_size
        global data
        global a
        # while True:
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += client_socket.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.COLOR_RGB2HLS)

        image = IMG.fromarray(frame)

        image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)

        w, h = image.height, image.width
        texture = Texture.create(size=(h, w))
        texture.blit_buffer(image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        # w_img = Image(size=(w, h), texture=texture)
        # if not a:
        self.stream.texture = texture

                # a = True
        # a = False


# class Test(Widget):
#     def __init__(self, **kwargs):
#         super(Test, self).__init__(**kwargs)
#         self.translate()
#
#         self.add_widget(w_img)
#
#     def translate(self):
#


kv = Builder.load_file("my.kv")

class DemoApp(App):
    def build(self):
        return Container()

if __name__ == '__main__':
    DemoApp().run()
