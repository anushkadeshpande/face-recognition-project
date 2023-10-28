from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox,QDialog
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QGridLayout, QApplication)
from PyQt5.QtGui import QCursor

import sys
class MessageBox():
    def __init__(self, msgType):
        self.msgWindow = QDialog()
        self.msgWindow.setWindowFlag(Qt.FramelessWindowHint)
        self.msgWindow.setStyleSheet("background-color: #fff;border : 1px solid #000;")
        self.closeWindowButton = QtWidgets.QToolButton(self.msgWindow)
        self.closeWindowButton.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
                border-radius: 10px;
            }
        """)
        self.closeWindowButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.closeWindowButton.setGeometry(QtCore.QRect(890, 10, 45, 45))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Assets/close-button.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeWindowButton.setIcon(icon)
        self.closeWindowButton.setIconSize(QtCore.QSize(35, 35))
        self.closeWindowButton.clicked.connect(lambda:self.msgWindow.close())
        
        self.msgWindow.setGeometry(500, 300, 950, 500)
     
        #)

        #if msgType == "creator-Info":
        #    self.msgBox.setText("This is the main text!")

    def button_clicked(self, s):
        print("click", s)

    def showMessageBox(self):    
        self.msgWindow.show()
        self.msgWindow.exec()
