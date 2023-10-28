from PageWindow import PageWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import sys
sys.path.append('../Backend')
from storeInformation import storeInformation
from validateData import validateData
from folder_exists import folder_exists
from PyQt5.QtCore import QObject, QThread, pyqtSignal

p1 = p2 = name = address = phone = email = None
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        global p1,p2, name,address,phone, email
        # add to firebase
        storeInformation(name, address, phone, email)
            
        ## MAKING FOLDERS FOR THE USER
        parent_dir1 = "./Datasets/Test/"+name
        parent_dir2 = "./Datasets/Train/"+name
        val_dir = "./Datasets/Validation/"+name
        p1 = folder_exists(parent_dir1)
        p2 = folder_exists(parent_dir2)
        p3 = folder_exists(val_dir)
        file1 = open("tmp.txt","w")
        file1.writelines([p1+"\n",p2+"\n",p3])
        file1.close()
        self.finished.emit()

class RegisterWindow(PageWindow):
    def __init__(self):
        super().__init__()
        dir_ = QtCore.QDir("Nunito")
        _id = QtGui.QFontDatabase.addApplicationFont("Assets/Nunito-VariableFont_wght.ttf")
        QtGui.QFontDatabase.applicationFontFamilies(_id)
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle("Register")
        self.UiComponents()

    def goToMain(self):
        self.goto("main")

    def show_loader(self):
        self.gif = QMovie('Assets/loader.gif')
        self.label.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setMovie(self.gif)
        self.gif.start()

    def startCapturing(self):
        self.goto("capture")

    def goToSurveillancePage(self):
        global p1
        global p2
        global name, phone, address, email
        #errMsg = ""
        errMsg = validateData(self.nameInput.toPlainText(), self.addressInput.toPlainText(), self.phoneInput.toPlainText(), self.emailInput.toPlainText())
    
        if errMsg:
            msg = QMessageBox()
            msg.setWindowTitle("Error!")
            msg.setText(errMsg)
            x = msg.exec_()  
        
        else:
            name = self.nameInput.toPlainText()
            phone = self.phoneInput.toPlainText()
            address = self.addressInput.toPlainText()
            email = self.emailInput.toPlainText()

            self.thread = QThread()
            self.worker = Worker()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(self.startCapturing)
        
            self.thread.start()

            self.show_loader()
            

    def UiComponents(self):
    
        self.nameLabel = QtWidgets.QLabel("Name  ", self)
        self.nameLabel.setFont(QFont('Nunito', 18))
        self.nameLabel.setGeometry(QtCore.QRect(125, 140, 100, 30))
        self.nameLabel.setStyleSheet('''
            QLabel{
                color:#FF8181;
                font-weight: bold;
            }
            ''')
        
        self.nameInput = QtWidgets.QTextEdit("" ,self)
        self.nameInput.setGeometry(QtCore.QRect(320, 120, 600, 55))
        self.nameInput.setStyleSheet('''
            QTextEdit{
                background-color : #F4F4F4;
                border: 1px solid transparent;
                border-radius:10px;
                padding:2px;
            }
            ''')
        self.nameInput.setFont(QFont('Nunito', 16))

        self.phoneLabel = QtWidgets.QLabel("Phone ", self)
        self.phoneLabel.setFont(QFont('Nunito', 18))
        self.phoneLabel.setGeometry(QtCore.QRect(125, 220, 100, 30))
        self.phoneLabel.setStyleSheet('''
            QLabel{
                color:#FF8181;
                font-weight: bold;
            }
            ''')
        
        self.phoneInput = QtWidgets.QTextEdit("" ,self)
        self.phoneInput.setGeometry(QtCore.QRect(320, 200, 600, 55))
        self.phoneInput.setStyleSheet('''
            QTextEdit{
                background-color : #F4F4F4;
                border: 1px solid transparent;
                border-radius:10px;
                padding:2px;
            }
            ''')
        self.phoneInput.setFont(QFont('Nunito', 16))


        self.emailLabel = QtWidgets.QLabel("Email  ", self)
        self.emailLabel.setFont(QFont('Nunito', 18))
        self.emailLabel.setGeometry(QtCore.QRect(125, 300, 100, 30))
        self.emailLabel.setStyleSheet('''
            QLabel{
                color:#FF8181;
                font-weight: bold;
            }
            ''')
        
        self.emailInput = QtWidgets.QTextEdit("" ,self)
        self.emailInput.setGeometry(QtCore.QRect(320, 280, 600, 55))
        self.emailInput.setStyleSheet('''
            QTextEdit{
                background-color : #F4F4F4;
                border: 1px solid transparent;
                border-radius:10px;
                padding:2px;
            }
            ''')
        self.emailInput.setFont(QFont('Nunito', 16))

        self.addressLabel = QtWidgets.QLabel("Address ", self)
        self.addressLabel.setFont(QFont('Nunito', 18))
        self.addressLabel.setGeometry(QtCore.QRect(125, 380, 200, 30))
        self.addressLabel.setStyleSheet('''
            QLabel{
                color:#FF8181;
                font-weight: bold;
            }
            ''')
        
        self.addressInput = QtWidgets.QTextEdit("" ,self)
        self.addressInput.setGeometry(QtCore.QRect(320, 360, 600, 200))
        self.addressInput.setStyleSheet('''
            QTextEdit{
                background-color : #F4F4F4;
                border: 1px solid transparent;
                border-radius:10px;
                padding:2px;
            }
            ''')
        self.addressInput.setFont(QFont('Nunito', 16))


        self.backButton = QtWidgets.QToolButton(self)
        self.backButton.setGeometry(QtCore.QRect(200, 620, 93, 28))
        self.backButton.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
            }
        """)
        self.backButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        backIcon = QtGui.QIcon()
        backIcon.addPixmap(QtGui.QPixmap("./Assets/back-button.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(backIcon)
        self.backButton.setIconSize(QtCore.QSize(200, 60))
        self.backButton.clicked.connect(self.goToMain)

        self.nextButton = QtWidgets.QToolButton(self)
        self.nextButton.setGeometry(QtCore.QRect(800, 620, 93, 40))
        self.nextButton.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
            }
        """)
        self.nextButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        nextIcon = QtGui.QIcon()
        nextIcon.addPixmap(QtGui.QPixmap("./Assets/next-button.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextButton.setIcon(nextIcon)
        self.nextButton.setIconSize(QtCore.QSize(200, 80))
        self.nextButton.clicked.connect(self.goToSurveillancePage)

        self.label = QtWidgets.QLabel(self)
        self.label.setStyleSheet('''
            QTextEdit{
                background-color : #ffffff00;
            }
        ''')
