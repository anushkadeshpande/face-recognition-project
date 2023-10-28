from PageWindow import PageWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor

class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.setWindowTitle("MainWindow")
        
    def initUI(self):
        self.UiComponents()

    def UiComponents(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.infoButton = QtWidgets.QToolButton(self)
        self.infoButton.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
                border-radius: 10px;
            }
        """)
        self.infoButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.infoButton.setGeometry(QtCore.QRect(30, 26, 70, 70))
        closeIcon = QtGui.QIcon()
        closeIcon.addPixmap(QtGui.QPixmap("./Assets/info-button.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.infoButton.setIcon(closeIcon)
        self.infoButton.setIconSize(QtCore.QSize(70, 70))
        self.infoButton.clicked.connect(lambda:self.goto("info"))

        self.registerUserButton = QtWidgets.QToolButton(self.centralwidget)
        
        self.registerUserButton.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
                border-radius: 20px;
            }
        """)
        self.registerUserButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.registerUserButton.setGeometry(QtCore.QRect(120, 200, 400, 400))
        self.registerUserButton.clicked.connect(self.make_handleButton("registerUserButton"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Assets/registration-icon3.jpg"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.registerUserButton.setIcon(icon)
        self.registerUserButton.setIconSize(QtCore.QSize(500, 500))
        self.registerUserButton.setToolTip("Register User")


        self.startSurveillanceButton = QtWidgets.QToolButton(self.centralwidget)
        
        self.startSurveillanceButton.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
                border-radius: 20px;
            }
        """)
        self.startSurveillanceButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.startSurveillanceButton.setGeometry(QtCore.QRect(690, 200, 400, 400))
        self.startSurveillanceButton.clicked.connect(self.make_handleButton("startSurveillanceButton"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Assets/surveillance-icon3.jpg"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startSurveillanceButton.setIcon(icon)
        self.startSurveillanceButton.setIconSize(QtCore.QSize(500, 500))
        self.startSurveillanceButton.setToolTip("Start Recognition")
        
        self.setCentralWidget(self.centralwidget)

    def make_handleButton(self, button):
        def handleButton():
            if button == "registerUserButton":
                self.goto("register")
                #self.goto("trainingScreen")
            
            elif button == "startSurveillanceButton":
                self.goto("startSurveillance")
        return handleButton