from PyQt5 import QtCore, QtGui, QtWidgets
from PageWindow import PageWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from runnerbkp import runner
from datetime import datetime

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""
        runner()
        self.finished.emit()

class TrainingScreenWindow(PageWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("")
        self.UiComponents()

    def show_loader(self):
        self.warningLabel.hide()
        self.startButton.hide()
        self.gif = QMovie('Assets/ani2.gif')
        self.label.setGeometry(QtCore.QRect(370, 150, 400, 500))
        self.label.setMovie(self.gif)
        self.anotherWarningLabel.show()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.gif.start()

    def start(self):
        self.startTime = datetime.now()
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.goToMain)
        
        self.thread.start()

        self.show_loader()

    @QtCore.pyqtSlot()
    def goToMain(self):
        self.endTime = datetime.now()
        start_time = self.startTime.strftime("%H:%M:%S")
        print("Start Time =", start_time)
        end_time = self.endTime.strftime("%H:%M:%S")
        print("End Time =", end_time)
        msgBox = QMessageBox()
        msgBox.setText("Model Trained Successfully Start: " + start_time + "End : "+ end_time)
        
        msgBox.exec_()
        self.goto("main")

    def UiComponents(self):
        self.startButton = QtWidgets.QToolButton(self)
        self.startButton.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
                border-radius: 10px;
            }
        """)
        self.startButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.startButton.setGeometry(QtCore.QRect(575, 50, 100, 100))
        camIcon = QtGui.QIcon()
        camIcon.addPixmap(QtGui.QPixmap("./Assets/start-icon.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startButton.setIcon(camIcon)
        self.startButton.setIconSize(QtCore.QSize(100, 100))
        self.startButton.clicked.connect(self.start)

        self.warningLabel = QtWidgets.QLabel("Click the button to start system training. \nThis may take a little longer than expected.",self)
        self.warningLabel.setGeometry(QtCore.QRect(340,150, 600,120))
        self.warningLabel.setFont(QFont('Nunito', 16))
        self.warningLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.label = QtWidgets.QLabel(self)

        self.anotherWarningLabel = QtWidgets.QLabel("Hold on. Model is getting trained...", self)
        self.anotherWarningLabel.setGeometry(QtCore.QRect(330,655, 600,120))
        self.anotherWarningLabel.setFont(QFont('Nunito', 16))
        self.anotherWarningLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.anotherWarningLabel.hide()