# 1. Import the necessary classes.
import cv2

# 2. Create a class for the camera and it's functions.
class Capture:

    def __init__(self, cam):
        self.photos = []
        self.count = []
        self.background_color = []
        self.border = []
        self.frame_text = ''
        self.font_size = 0
        self.camera = cam

    def open_camera(self):
        cam = self.camera
        cv2.namedWindow("Photobooth")
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to grab frame")
                break
            cv2.imshow("Photobooth", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break        
        cam.release()
        cv2.destroyAllWindows()
open_cam = Capture(cv2.VideoCapture(0))
open_cam.open_camera()

# 3. Create a class for the Layout of the photobooth.

# 4. Create a class for saving the photos.