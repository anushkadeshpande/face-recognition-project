import cv2

class Camera:
    def __init__(self, camera):
        self.camera = camera
        self.cap = None

    def openCamera(self):
        self.vc = cv2.VideoCapture(0)
        # vc.set(5, 30)  #set FPS
        self.vc.set(3, 640)  # set width
        self.vc.set(4, 480)  # set height

        if not self.vc.isOpened():
            print('failure')
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return

    def closeCamera(self):
        self.vc.release()