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

    def take_photos(self):
        cv2.namedWindow("Photobooth")
        while self.count < 4:
            ret, frame = self.read_frame()
            if not ret:
                break
            cv2.imshow("Photobooth", frame)
            key = cv2.waitKey(1)
            if key % 256 == 27:  # ESC
                print("Escape pressed.")
                return False
            elif key % 256 == 32:  # SPACE
                self.photos.append(frame)
                print(f"Photo {self.count + 1} taken")
                self.count += 1
        return True

    def create_collage(self):
        target_width = 200
        resized_photos = [cv2.resize(photo, (target_width, int(photo.shape[0] * target_width / photo.shape[1])))
                        for photo in self.photos]
        
        collage = np.vstack(resized_photos)

        h, w = collage.shape[:2]
        bg = np.full((h + 2*self.border, w + 2*self.border, 3), self.background_color, dtype=np.uint8)
        bg[self.border:self.border+h, self.border:self.border+w] = collage
        cv2.rectangle(bg, (self.border, self.border), (bg.shape[1]-self.border, bg.shape[0]-self.border), (0, 0, 0), 5)
        return bg
    
    def add_text(self, image):
        pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)

        bbox = draw.textbbox((0, 0), self.frame_text, font=self.font)
        text_width = bbox[2] - bbox[0]
        pos = ((pil_img.width - text_width) // 2, self.border // 2)
        offset = 2

        for dx in [-offset, offset]:
            for dy in [-offset, offset]:
                draw.text((pos[0] + dx, pos[1] + dy), self.frame_text, font=self.font, fill=(0, 0, 0))

        draw.text(pos, self.frame_text, font=self.font, fill=(255, 255, 0))
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
# 4. Create a class for saving the photos.
class PhotoSaving:
    def __init__(self, final_img):
        self.final_img = final_img

    def ask_save(self):
        cv2.imshow("Our Memories!", self.final_img)
        print("Do you want to save (s) or discard (d)?")
        while True:
            key = cv2.waitKey(1)
            if key % 256 == 27:
                print("Exited.")
                break
            elif key % 256 == ord('s'):
                cv2.imwrite("Memories.png", self.final_img)
                print("Saved!")
                break
            elif key % 256 == ord('d'):
                print("Photo discarded.")
                break

# 5. Create a separate class for the main app.

class PhotoBoothSystem:
    def __init__(self):
        self.layout = LayOut(cv2.VideoCapture(0))

    def start(self):
        while True:
            success = self.layout.take_photos()
            if not success or len(self.layout.photos) < 4:
                break

            collage = self.layout.create_collage()
            collage_with_text = self.layout.add_text(collage)

            saver = PhotoSaving(collage_with_text)
            saver.ask_save()

            again = messagebox.askyesno("Try Again?", "Do you want to take more photos?")
            if not again:
                break
            self.layout.count = 0
            self.layout.photos.clear()

        self.layout.release()
        print("Thanks for using the photobooth!")

# 6. Make use of that tkinter library.
def run_gui():
    root = tk.Tk()
    root.title("OOP DIY Photobooth")
    root.geometry("400x300")
    root.configure(bg="#fff0f5")

    label = tk.Label(root, text="📸 Welcome to the DIY Photobooth!", font=("Arial", 14), bg="#fff0f5")
    label.pack(pady=30)

    def start_photobooth():
        root.withdraw()
        app = PhotoBoothSystem()
        app.start()
        root.deiconify()

    btn = tk.Button(root, text="Start Photobooth", command=start_photobooth, font=("Arial", 13), bg="#ffb6c1", width=20)
    btn.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    run_gui()