import os
import cv2
from PageWindow import PageWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QApplication, QHBoxLayout, QMessageBox
import os
import pickle
from PIL import Image
import base64
from io import BytesIO
import numpy
import json
import random
from statistics import mode
import cv2
from keras.models import Model
from keras.models import load_model
from PIL import Image
import tensorflow.keras.backend as K
import numpy as np
#from mtcnn.mtcnn import MTCNN
import sys
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from findCosineDistance import findCosineDistance
sys.path.append('../Backend')
from face_extractor import face_extractor
from compareEmbeddings import compareEmbeddings
from PyQt5.QtGui import * 
from datetime import datetime
from logUnknown import logUnknown
from findUniqueUnknown import findUniqueUnknown
from Camera import Camera
import dlib

camera = Camera(0)

vggface= model_feature_vggface= model_feature_facenet= model_feature_facenet512= face_cascade=model_feature_arcface = None
model_facenet512= model_facenet= model_vggface= person_rep= model_arcface = None
val_vgg = val_facenet = val_facenet_512 = val_dlib =val_arcface= None
unknown_emb = None

model_dlib = model_dlib_final = None

def loadModels():
    global vggface, model_feature_vggface, model_feature_facenet, model_feature_facenet512,model_feature_arcface, face_cascade
    global model_facenet512, model_facenet, model_vggface, person_rep, model_arcface
    global val_vgg, val_facenet, val_facenet_512 , val_dlib,val_arcface
    global unknown_emb
    global model_dlib, model_dlib_final

    unknown_emb = []
    from tensorflow.keras.applications.imagenet_utils import preprocess_input
    from keras.preprocessing import image
    from tensorflow.keras.preprocessing.image import load_img,img_to_array
    import tensorflow as tf
    import dlib
    
    vggface=load_model('Backend/Core/Generations/models/feature_extractor_model.h5')
    model_feature_vggface=Model(inputs=vggface.layers[0].input,outputs=vggface.layers[-2].output)
    model_feature_facenet=load_model('Backend/Core/Generations/models/feature_extractor_model_facenet.h5')
    model_feature_facenet512=load_model('Backend/Core/Generations/models/feature_extractor_model_facenet_512.h5')
    model_feature_arcface=load_model('Backend/Core/Generations/models/feature_extractor_model_arcface.h5')
    face_cascade = cv2.CascadeClassifier('Dependencies/haarcascade_frontalface_default.xml')
    model_dlib = dlib.face_recognition_model_v1("Backend/Core/Dependencies/dlib_face_recognition_resnet_model_v1.dat")
    
    model_facenet512 = pickle.load(open('Backend/Core/Generations/classifierModels/finalized_model_512.sav', 'rb'))
    model_facenet = pickle.load(open('Backend/Core/Generations/classifierModels/finalized_model.sav', 'rb'))
    model_vggface = pickle.load(open('Backend/Core/Generations/classifierModels/finalized_model_vggface.sav', 'rb'))
    model_dlib_final = pickle.load(open('Backend/Core/Generations/classifierModels/finalized_model_dlib_resnet.sav', 'rb'))
    model_arcface = pickle.load(open('Backend/Core/Generations/classifierModels/finalized_model_arcface.sav', 'rb'))

    val_vgg = np.load('Backend/Core/Generations/ValidationEmbeddings/val_vgg.npy')
    val_facenet = np.load('Backend/Core/Generations/ValidationEmbeddings/val_facenet.npy')
    val_facenet_512 = np.load('Backend/Core/Generations/ValidationEmbeddings/val_facenet_512.npy')
    val_dlib = np.load('Backend/Core/Generations/ValidationEmbeddings/val_dlib_resnet.npy')
    val_arcface = np.load('Backend/Core/Generations/ValidationEmbeddings/val_arcface.npy')

    for unknown_pic in os.listdir('./Capture'):
        unknown_face = cv2.imread('./Capture/'+unknown_pic)
        val_emb = find_embedding("facenet_512",model_feature_facenet512, cv2.resize(unknown_face,(160,160)))
        unknown_emb.append(val_emb)
    print(len(unknown_emb))
    person_folders=os.listdir('Datasets/Train')
    person_rep=dict()
    for i,person in enumerate(person_folders):
        person_rep[i]=person

    print(person_rep)

def find_embedding(model,feature_model, img):    
    if model == 'dlib_resnet':
        dlib_model = dlib.face_recognition_model_v1("Backend/Core/Dependencies/dlib_face_recognition_resnet_model_v1.dat")
        img=dlib_model.compute_face_descriptor(img)
        img_representation=np.array(img)
        return img_representation   
    else:
        if model == "facenet" or model=="facenet512":
            face_pixels = img.astype('float32')
            mean, std = face_pixels.mean(), face_pixels.std()
            face_pixels = (face_pixels - mean) / std
            sample_img = np.expand_dims(face_pixels, axis=0)
        elif model == "arcface":
            img = img.astype(np.float32) / 255.
            if len(img.shape) == 3:
                sample_img = np.expand_dims(img, 0)    
        else:
            sample_img = np.expand_dims(img, axis=0)
        yhat = feature_model.predict(sample_img)
        return yhat


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        loadModels()
        self.finished.emit()

class SurveillanceWindow(PageWindow):
    global val_vgg, val_facenet, val_facenet_512, val_dlib, val_arcface, person_rep
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.camera = camera
        self.predCount = [0 for _ in range(5)]
        self.unknown = [0 for _ in range(5)]
        # Create a timer.
        self.timer = QTimer()

        self.timer.timeout.connect(self.nextFrameSlot)

    def initUI(self):
        self.setWindowTitle("Face Recognition")
        self.UiComponents()
        
    def restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)

    def computeResult(self,face, personCount):
        
        self.vgg_emb=find_embedding("vggface",model_feature_vggface,cv2.resize(face,(224,224)))
        self.class_index_vggface, self.class_probability_vggface = compareEmbeddings(model_vggface, self.vgg_emb)
        print('\nPrediction Probablity of vggface:%.3f' %(self.class_probability_vggface))
        
        self.facenet_emb=find_embedding("facenet", model_feature_facenet,cv2.resize(face,(160,160)))
        self.class_index_facenet, self.class_probability_facenet = compareEmbeddings(model_facenet, self.facenet_emb)
        print('Prediction Probablity of facenet:%.3f' %(self.class_probability_facenet))
                
        self.facenet512_emb=find_embedding("facenet512",model_feature_facenet512, cv2.resize(face,(160,160)))
        self.class_index_facenet512, self.class_probability_facenet512 = compareEmbeddings(model_facenet512, self.facenet512_emb)
        print('Prediction Probablity of facenet512:%.3f' %(self.class_probability_facenet512))

        self.dlib_emb=find_embedding("dlib_resnet",model_dlib_final, cv2.resize(face,(150,150)))
        print("\ndlib_emb before",self.dlib_emb)
        self.dlib_emb=np.reshape(self.dlib_emb,(1,128))
        print("\ndlib_emb shape after",self.dlib_emb.shape)
        self.class_index_dlib, self.class_probability_dlib = compareEmbeddings(model_dlib_final, self.dlib_emb)
        print('Prediction Probablity of dlib resnet:%.3f' %(self.class_probability_dlib))

        self.arcface_emb=find_embedding("arcface",model_feature_arcface,cv2.resize(face,(112,112)))
        self.class_index_arcface, self.class_probability_arcface = compareEmbeddings(model_arcface, self.arcface_emb)
        print('\nPrediction Probablity of arcface:%.3f' %(self.class_probability_arcface))

        self.tuple_index=(self.class_index_vggface, self.class_index_facenet, self.class_index_facenet512,self.class_index_dlib,self.class_index_arcface)
        self.final_pred =mode(self.tuple_index)
        self.name=person_rep[self.final_pred]
        print("\nclass:",self.name)

        j = self.final_pred * 10
                
        for i in range(j, (j+10)):
            
            self.cos_dist_vggface=findCosineDistance(self.vgg_emb[0],val_vgg[i])
            print("\ncosinedist vggface",person_rep[self.final_pred],":",self.cos_dist_vggface)
            if(self.cos_dist_vggface>0.28):
                self.count1+=1
            
            self.cos_dist_facenet=findCosineDistance(self.facenet_emb[0],val_facenet[i])
            print("\ncosinedist facenet",person_rep[self.final_pred],":",self.cos_dist_facenet)
            if(self.cos_dist_facenet>0.35):
                self.count2+=1
                        
            print(self.facenet512_emb[0].shape)
            print(val_facenet_512[i].shape)
            self.cos_dist_facenet512=findCosineDistance(self.facenet512_emb[0],val_facenet_512[i])
            print("\ncosinedist facenet512",person_rep[self.final_pred],":",self.cos_dist_facenet512)
            if(self.cos_dist_facenet512>0.3):
                self.count3+=1  
            
            print(self.dlib_emb[0].shape)
            print(val_dlib.shape)
            print(val_dlib[i].shape)
            self.cos_dist_dlib=findCosineDistance(self.dlib_emb[0],val_dlib[i])
            print("\ncosinedist dlib",person_rep[self.final_pred],":",self.cos_dist_dlib)
            if(self.cos_dist_dlib>0.057):
                self.count4+=1

            self.cos_dist_arcface=findCosineDistance(self.arcface_emb[0],val_arcface[i])
            print("\ncosinedist arcface",person_rep[self.final_pred],":",self.cos_dist_arcface)
            if(self.cos_dist_arcface>0.4):
                self.count5+=1
            
            self.prob1=self.count1/10
            print("\nProbability vggface:",self.prob1)
                        
            if(self.prob1>0.6):
                self.unknown_vggface=1
                  
            else:
                self.unknown_vggface=0
                    
            self.prob2=self.count2/10
            print("\nProbability facenet:",self.prob2)
            
            if(self.prob2>0.6):
                self.unknown_facenet=1
                
            else:
                self.unknown_facenet=0
                
            self.prob3=self.count3/10
            print("\nProbability facenet512:",self.prob3)
            
            if(self.prob3>0.6):
                self.unknown_facenet512=1
                
            else:
                self.unknown_facenet512=0

            self.prob4=self.count4/10
            print("\nProbability dlib:",self.prob4)
            
            if(self.prob4>0.6):
                self.unknown_dlib=1
                
            else:
                self.unknown_dlib=0               


            self.prob5=self.count5/10
            print("\nProbability arcface:",self.prob5)
                        
            if(self.prob5>0.6):
                self.unknown_arcface=1
                  
            else:
                self.unknown_arcface=0
                      

            self.unknown_tuple=(self.unknown_vggface,self.unknown_facenet,self.unknown_facenet512, self.unknown_dlib,self.unknown_arcface)
            self.unknown[personCount]=mode(self.unknown_tuple)

    def show_loader(self):
        self.btnCamera.hide()
        self.btnLabel.hide()
        self.gif = QMovie('Assets/loader.gif')
        self.label.setGeometry(QtCore.QRect(510, 350, 150, 150))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setMovie(self.gif)
        self.gif.start()
                

    def start(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.startCamera)
        
        self.thread.start()

        self.show_loader()


    def startCamera(self):
        self.label.hide()
        self.homeButton.show()
        camera.openCamera()
        
        self.timer.start(int(1000. / 24))

    def goToMain(self):
        self.timer.stop()
        camera.closeCamera()
        self.restart()

    def nextFrameSlot(self):
        global unknown_emb
        rval, frame = camera.vc.read()
        self.result = face_cascade.detectMultiScale(frame, 1.3, 5)
        self.count1=0
        self.count2=0
        self.count3=0
        self.count4=0
        self.count5=0
        

        if type(self.result) is np.ndarray:
            print("No. of people : ", len(self.result))
            
            for i, (x, y, w, h) in enumerate(self.result):
                print(i)
                #face = frame[y:y+h, x:x+w]
                y=y-10
                h=h+15
                face = frame[y:y+h, x:x+w]
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) 
                
                print("2. Face extracted")
                self.computeResult(face, i)
                if self.unknown[i]==1:
                    self.predCount[i] += 1
                    cv2.putText(frame,"Unknown",(x, y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)

                    if self.predCount[i] == 5:
                        now = datetime.now()
                        date_time = now.strftime("%m%d%Y%H%M%S")
                        if not os.path.exists('./Capture'):
                            os.makedirs('./Capture')
                            #face = cv2.resize(face, (400, 400))
                            cv2.imwrite('./Capture/'+date_time+'.png', face)
                            logUnknown()
                        else:
                            print(len(os.listdir('./Capture')))
                            temp = findUniqueUnknown(unknown_emb, face)
                            if temp:
                                #face = cv2.resize(face, (400, 400))
                                cv2.imwrite('./Capture/'+date_time+'.png', face)
                                logUnknown(len(os.listdir('./Capture')))
                                unknown_emb = temp
                                #start a thread here
                                # show a loader and simultaneously check for dupicate unkown and send out notification
                        self.predCount[i] = 0
                        self.unknown[i] = 0
                    
                else:
                    self.predCount[i] = 0
                    self.unknown[i] = 0
                    cv2.putText(frame,person_rep[self.final_pred],(x, y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
                    #cv2.putText(frame,person_rep[final_pred],(bounding_box[0], bounding_box[1]-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)

        showframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(showframe, showframe.shape[1], showframe.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        self.cameraWindow.setPixmap(pixmap)
    
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

        self.btnLabel = QtWidgets.QLabel("Click on the camera button to start surveillance", self)
        self.btnLabel.setGeometry(QtCore.QRect(320,150, 600,60))
        self.btnLabel.setFont(QFont('Nunito', 16))
        self.btnLabel.setAlignment(QtCore.Qt.AlignCenter)

        #self.start()
        
        self.cameraWindow = QtWidgets.QLabel(self)
        self.cameraWindow.setGeometry(QtCore.QRect(270, 200, 640, 480))

        self.label = QtWidgets.QLabel(self)

        self.homeButton = QtWidgets.QToolButton(self)
        self.homeButton.setGeometry(QtCore.QRect(550, 680, 100, 50))
        self.homeButton.setStyleSheet("""
            QToolButton {
                border : 1px solid transparent;
            }
        """)
        self.homeButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        homeIcon = QtGui.QIcon()
        homeIcon.addPixmap(QtGui.QPixmap("./Assets/home-button.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.homeButton.setIcon(homeIcon)
        self.homeButton.setIconSize(QtCore.QSize(100, 50))
        self.homeButton.clicked.connect(self.goToMain)
        self.homeButton.hide()