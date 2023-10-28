from Components.PageWindow import PageWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PageWindow import PageWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

class InfoWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("")
        self.UiComponents()

    def UiComponents(self):
        self.infoLabel = QtWidgets.QLabel("",self)
        self.pixmap = QPixmap('Assets/info.png')
        #self.pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        #self.pixmap.scaled(64,64,Qt.KeepAspectRatio)
        # adding image to label
        self.infoLabel.setPixmap(self.pixmap)

        # Optional, resize label to image size
        self.infoLabel.setGeometry(QtCore.QRect(270, 150, 700, 450))
        #self.infoLabel.resize(500, 500)

        self.backButton = QtWidgets.QToolButton(self)
        
        self.backButton.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
            }
        """)
        
        self.backButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.setGeometry(QtCore.QRect(520, 650, 200, 60))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Assets/back-button.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(icon)
        self.backButton.setIconSize(QtCore.QSize(200, 60))
        self.backButton.clicked.connect(lambda:self.goto("main"))
 
