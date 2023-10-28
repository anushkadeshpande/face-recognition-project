#from PySide2.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget
from PageWindow import PageWindow
from PyQt5.QtCore import Qt, QPoint
from Camera import Camera
from MainWindow import MainWindow
from RegisterWindow import RegisterWindow
from CaptureWindow import CaptureWindow
from TrainingScreenWindow import TrainingScreenWindow
from SurveillanceWindow import SurveillanceWindow
from InfoWindow import InfoWindow
from PyQt5.QtGui import QCursor

from MessageBox import MessageBox

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.m_pages = {}

        self.closeWindowButton = QtWidgets.QToolButton(self)
        self.closeWindowButton.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
                border-radius: 10px;
            }
        """)
        self.closeWindowButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.closeWindowButton.setGeometry(QtCore.QRect(1100, 26, 70, 70))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Assets/close-button.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeWindowButton.setIcon(icon)
        self.closeWindowButton.setIconSize(QtCore.QSize(70, 70))
        self.closeWindowButton.clicked.connect(lambda:self.close())

        self.register(MainWindow(), "main")
        self.register(RegisterWindow(), "register")
        self.register(SurveillanceWindow(), "startSurveillance")
        self.register(CaptureWindow(), "capture")
        self.register(TrainingScreenWindow(), "trainingScreen")
        self.register(InfoWindow(), "info")

        self.setStyleSheet("background-color: #fff")
        self.oldPos = self.pos()
        self.goto("main")


    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())
        
    def showInfo(self):
        msgBox = MessageBox("creator-Info")
        msgBox.showMessageBox()

    def center(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = sg.width() - 0.8*sg.width()
        y = sg.height() - 0.9*sg.height()
        self.move(int(x), int(y))

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
