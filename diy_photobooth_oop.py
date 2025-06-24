# 1. Import the necessary classes.
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import messagebox

# 2. Create a class for the camera and it's functions.
class Capture:

    def __init__(self, cam):
        self.camera = cam

    def read_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            print("Failed to grab frame")
        return ret, frame
    
    def release(self):
        self.camera.release()
        cv2.destroyAllWindows()

# 3. Create a class for the Layout of the photobooth.
class LayOut(Capture):
    def __init__(self, cam):
        super().__init__(cam)
        self.photos = []
        self.count = 0
        self.background_color = (244, 194, 194)
        self.border = 100
        self.frame_text = 'Our Memories'
        self.font_file = "Lobster-Regular.ttf"
        self.font_size = 50
        self.font = self.load_font()

    def load_font(self):
        try:
            return ImageFont.truetype(self.font_file, self.font_size)
        except IOError:
            print("Font not found. Using default.")
            return ImageFont.load_default()


# 4. Create a class for saving the photos.
