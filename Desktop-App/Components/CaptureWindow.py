import os
import cv2
from PageWindow import PageWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QApplication, QHBoxLayout, QMessageBox
import sys
from face_extractor import face_extractor


from Camera import Camera

camera = Camera(0)
class CaptureWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.camera = camera
        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        cap = cv2.VideoCapture(0)
        self.framerate = cap.get(cv2.CAP_PROP_FPS)
        self.framecount = 0
        self.count = 0

    def getDirectories(self):
        file1 = open("tmp.txt","r+") 
        
        dir_list = file1.readlines()
        file1.close()
        self.p1 = dir_list[0][:-1]
        self.p2 = dir_list[1][:-1]
        self.p3 = dir_list[2]
        os.remove("tmp.txt")

    def initUI(self):
        self.setWindowTitle("Capture")
        self.UiComponents()

    def goToMain(self):
        self.goto("main")

    def start(self):
        self.btnCamera.hide()
        self.btnLabel.hide()
        self.getDirectories()
        camera.openCamera()
           
        self.timer.start(int(1000. / 24))

    def nextFrameSlot(self):
        rval, frame = camera.vc.read()
        self.framecount += 1
        if self.framecount == (self.framerate * 0.20):
            self.framecount = 0
            if face_extractor(frame) is not None:
                self.count += 1
                face = cv2.resize(face_extractor(frame), (400, 400))
                #face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    
                
                if ( self.count <= 10 ):
                    file_name_path = self.p1 +'/' + str(self.count) + '.jpg'
            
                elif ( self.count <= 20 ):
                    file_name_path = self.p3 +'/' + str(self.count) + '.jpg'

                else:
                    file_name_path = self.p2 +'/' + str(self.count) + '.jpg'
                cv2.imwrite(file_name_path, face)
        cv2.putText(frame, str(self.count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
          
            #else:
                #print("Face not found")
                #pass
        
        showframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(showframe, showframe.shape[1], showframe.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.cameraWindow.setPixmap(pixmap)

        if self.count == 60 :
            self.timer.stop()
            msgBox = QMessageBox()
            msgBox.setText("Images Captured Successfully!")
            msgBox.exec_()
            camera.closeCamera()
            if len(os.listdir('./Datasets/Train')) > 1:
                self.goto("trainingScreen")
            else:
                msgBox = QMessageBox()
                msgBox.setText("Add atleast one more class to train the model!")
                msgBox.exec_()
                self.goto("main")

    
    def UiComponents(self):

        self.btnCamera = QtWidgets.QToolButton(self)
        self.btnCamera.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
                border-radius: 10px;
            }
        """)
        self.btnCamera.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnCamera.setGeometry(QtCore.QRect(550, 50, 100, 100))
        camIcon = QtGui.QIcon()
        camIcon.addPixmap(QtGui.QPixmap("./Assets/cam-icon.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCamera.setIcon(camIcon)
        self.btnCamera.setIconSize(QtCore.QSize(100, 90))
        self.btnCamera.clicked.connect(self.start)

        self.btnLabel = QtWidgets.QLabel("Click on the camera button to start capturing", self)
        self.btnLabel.setGeometry(QtCore.QRect(350,150, 600,60))
        self.btnLabel.setFont(QFont('Nunito', 16))
        
        self.cameraWindow = QtWidgets.QLabel(self)
        self.cameraWindow.setGeometry(QtCore.QRect(270, 200, 640, 480))


