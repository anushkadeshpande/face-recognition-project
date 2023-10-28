# Face Recognition
# Importing the libraries
import os
import pickle
from PIL import Image
import base64
from io import BytesIO
import json
import random
from statistics import mode
import cv2
from keras.models import Model
from keras.models import load_model
from PIL import Image
import tensorflow.keras.backend as K
import numpy as np
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img,img_to_array
import tensorflow as tf
from mtcnn.mtcnn import MTCNN
detector = MTCNN()
with tf. device("cpu:0"):
    vggface=load_model('./Generations/models/feature_extractor_model.h5')
    model_feature_vggface=Model(inputs=vggface.layers[0].input,outputs=vggface.layers[-2].output)
    model_feature_facenet=load_model('./Generations/models/feature_extractor_model_facenet.h5')
    model_feature_facenet512=load_model('./Generations/models/feature_extractor_model_facenet_512.h5')
    face_cascade = cv2.CascadeClassifier('../../Dependencies/haarcascade_frontalface_default.xml')
    
    
    filename = './Generations/classifierModels/finalized_model_512.sav'
    model_facenet512 = pickle.load(open(filename, 'rb'))
    
    
    filename = './Generations/classifierModels/finalized_model.sav'
    model_facenet = pickle.load(open(filename, 'rb'))
    
    
    filename = './Generations/classifierModels/finalized_model_vggface.sav'
    model_vggface = pickle.load(open(filename, 'rb'))
    

    def embedding_vggface(img):
        sample_img = np.expand_dims(img, axis=0)
        yhat = model_feature_vggface.predict(sample_img)
        return yhat
    
    
    def embedding_facenet(img):
        face_pixels = img.astype('float32')
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        sample_img = np.expand_dims(face_pixels, axis=0)
        yhat = model_feature_facenet.predict(sample_img)
        return yhat
    
    
    def embedding_facenet512(img):
        face_pixels = img.astype('float32')
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        sample_img = np.expand_dims(face_pixels, axis=0)
        yhat = model_feature_facenet512.predict(sample_img)
        return yhat
    val_vgg = []
    val_facenet = []
    val_facenet_512 = []
    def findValidationEmbeddings():
        global val_vgg
        global val_facenet
        global val_facenet_512

        for person in os.listdir("../../Datasets/Validation_set"):
            for img in os.listdir("../../Datasets/Validation_set/"+person):
                face1="../../Datasets/Validation_set/"+person+'/'+img
                face = cv2.imread(face1)
                #print(face1)
                val_vgg.append(embedding_vggface(cv2.resize(face,(224,224))))
                val_facenet.append(embedding_facenet(cv2.resize(face,(160,160))))
                val_facenet_512.append(embedding_facenet512(cv2.resize(face,(160,160))))


    findValidationEmbeddings()
    person_folders=os.listdir('../../Datasets/Train')
    person_rep=dict()
    for i,person in enumerate(person_folders):
      person_rep[i]=person
      
    print(person_rep)
    
    def findCosineDistance(source_representation, test_representation):
        a = np.matmul(np.transpose(source_representation), test_representation)
        b = np.sum(np.multiply(source_representation, source_representation))
        c = np.sum(np.multiply(test_representation, test_representation))
        return 1 - (a / (np.sqrt(b) * np.sqrt(c)))
     
    cap = cv2.VideoCapture(0)
    
    while True:
        __, frame = cap.read()

        result = face_cascade.detectMultiScale(frame, 1.3, 5)
        count1=0
        count2=0
        count3=0
        if type(result) is np.ndarray:
            for i, (x, y, w, h) in enumerate(result):
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) 
                y=y-10
                h=h+15
                face = frame[y:y+h, x:x+w]
                print("2. Face extracted")
                
                vgg_emb=embedding_vggface(cv2.resize(face,(224,224)))
                facenet_emb=embedding_facenet(cv2.resize(face,(160,160)))
                facenet512_emb=embedding_facenet512(cv2.resize(face,(160,160)))

                yhat_class_vggface = model_vggface.predict(vgg_emb)
                yhat_prob_vggface = model_vggface.predict_proba(vgg_emb)
                class_index_vggface = yhat_class_vggface[0]
                class_probability_vggface = yhat_prob_vggface[0,class_index_vggface] * 100
                print('\nPrediction Probablity of vggface:%.3f' %(class_probability_vggface))
                
                yhat_class_facenet = model_facenet.predict(facenet_emb)
                yhat_prob_facenet = model_facenet.predict_proba(facenet_emb)
                class_index_facenet = yhat_class_facenet[0]
                class_probability_facenet = yhat_prob_facenet[0,class_index_facenet] * 100 
                print('Prediction Probablity of facenet:%.3f' %(class_probability_facenet))
               
                yhat_class_facenet512 = model_facenet512.predict(facenet512_emb)
                yhat_prob_facenet512 = model_facenet512.predict_proba(facenet512_emb)
                class_index_facenet512 = yhat_class_facenet512[0]
                class_probability_facenet512 = yhat_prob_facenet512[0,class_index_facenet512] * 100
                print('Prediction Probablity of facenet512:%.3f' %(class_probability_facenet512))
    
                tuple_index=(class_index_vggface, class_index_facenet, class_index_facenet512)
                final_pred =mode(tuple_index)
                name=person_rep[final_pred]
                print("\nclass:",name)
                
                j = final_pred * 10

                for i in range(j, (j+10) ):
                    print("\nface:",person_rep[final_pred])
                    cos_dist_vggface=findCosineDistance(vgg_emb[0],val_vgg[i][0])
                    print("\ncosinedist vggface",person_rep[final_pred],":",cos_dist_vggface)
                    if(cos_dist_vggface>0.35):
                        count1+=1
                    
                    cos_dist_facenet=findCosineDistance(facenet_emb[0],val_facenet[i][0])
                    print("\ncosinedist facenet",person_rep[final_pred],":",cos_dist_facenet)
                    if(cos_dist_facenet>0.50):
                        count2+=1
                        
                    cos_dist_facenet512=findCosineDistance(facenet512_emb[0],val_facenet_512[i][0])
                    print("\ncosinedist facenet512",person_rep[final_pred],":",cos_dist_facenet512)
                    if(cos_dist_facenet512>0.55):
                        count3+=1
                    
                prob1=count1/10
                print("\nProbability vggface:",prob1)
                    
                if(prob1>0.6):
                    unknown_vggface=1
                else:
                    unknown_vggface=0
                    
                prob2=count2/10
                print("\nProbability facenet:",prob2)
                    
                if(prob2>0.6):
                    unknown_facenet=1
                else:
                    unknown_facenet=0
               
                prob3=count3/10
                print("\nProbability:",prob3)
        
                if(prob3>0.6):
                    unknown_facenet512=1
                else:
                    unknown_facenet512=0               
               
                unknown_tuple=(unknown_vggface,unknown_facenet,unknown_facenet512)
                unknown=mode(unknown_tuple)
                if unknown==1:
                    cv2.putText(frame,"Unknown",(x, y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
                    
                else:
                    cv2.putText(frame,person_rep[final_pred],(x, y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
                    
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) &0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
