# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 22:31:32 2022

@author: Bhavini
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 23:19:21 2022

@author: Sharayu
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 19:41:20 2022

@author: Bhavini
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 22:59:02 2021

@author: Bhavini
"""

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
    vggface=load_model('feature_extractor_model.h5')
    model_feature_vggface=Model(inputs=vggface.layers[0].input,outputs=vggface.layers[-2].output)
    model_feature_facenet=load_model('feature_extractor_model_facenet.h5')
    model_feature_facenet512=load_model('feature_extractor_model_facenet_512.h5')
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    
    filename = 'finalized_model_512.sav'
    model_facenet512 = pickle.load(open(filename, 'rb'))
    
    
    filename = 'finalized_model.sav'
    model_facenet = pickle.load(open(filename, 'rb'))
    
    
    filename = 'finalized_model_vggface.sav'
    model_vggface = pickle.load(open(filename, 'rb'))
    
    
    
    def embedding_vggface(img):
        #face_pixels = img.astype('float32')
        #mean, std = face_pixels.mean(), face_pixels.std()
        #face_pixels = (face_pixels - mean) / std
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
    
    person_folders=os.listdir('Datasets8/Train')
    person_rep=dict()
    for i,person in enumerate(person_folders):
      person_rep[i]=person
      
    print(person_rep)
    
    def findCosineDistance(source_representation, test_representation):
        a = np.matmul(np.transpose(source_representation), test_representation)
        b = np.sum(np.multiply(source_representation, source_representation))
        c = np.sum(np.multiply(test_representation, test_representation))
        return 1 - (a / (np.sqrt(b) * np.sqrt(c)))
    
    '''import pickle
    person_rep=dict()
    person_list_file = open("namelist", "rb")
    person_rep = pickle.load(person_list_file)
    print(person_rep)'''
    
    cap = cv2.VideoCapture(0)
    
    while True:
        __, frame = cap.read()
        #canvas = detect(gray, frame)
        #image, face =face_detector(frame)
        
        #result = face_extractor(frame)
        
        result = face_cascade.detectMultiScale(frame, 1.3, 5)
        count=0
        #print('result',result)
        if type(result) is np.ndarray:
        #if result != []:
            for i, (x, y, w, h) in enumerate(result):
                #print(person)
                #bounding_box = person['box']
                #print('\ni',i)
                #print('\nx y w h',x,y,w,h)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) 
                y=y-10
                h=h+15
                face = frame[y:y+h, x:x+w]
                # extract the face
                #face = frame[y1:y2, x1:x2]
                print("2. Face extracted")
                #resized for FaceNet model
                
                vgg_emb=embedding_vggface(cv2.resize(face,(224,224)))
                facenet_emb=embedding_facenet(cv2.resize(face,(160,160)))
                facenet512_emb=embedding_facenet512(cv2.resize(face,(160,160)))
                
                
                #comparing the embeddings
                yhat_class_vggface = model_vggface.predict(vgg_emb)
                #print("\npredicted embedding:",yhat_class_vggface)
                #print("\npredicted embedding1:",yhat_class_vggface[0])
                #Retrieving the probability of the prediction
                yhat_prob_vggface = model_vggface.predict_proba(vgg_emb)
                #print("4. Predicting class and probability done")
                class_index_vggface = yhat_class_vggface[0]
                class_probability_vggface = yhat_prob_vggface[0,class_index_vggface] * 100
                
                print('\nPrediction Probablity of vggface:%.3f' %(class_probability_vggface))
                
    
                
                #comparing the embeddings
                yhat_class_facenet = model_facenet.predict(facenet_emb)
                #Retrieving the probability of the prediction
                yhat_prob_facenet = model_facenet.predict_proba(facenet_emb)
                #print("4. Predicting class and probability done")
                class_index_facenet = yhat_class_facenet[0]
                class_probability_facenet = yhat_prob_facenet[0,class_index_facenet] * 100
                
                print('Prediction Probablity of facenet:%.3f' %(class_probability_facenet))
                
                
                
               
                #comparing the embeddings
                yhat_class_facenet512 = model_facenet512.predict(facenet512_emb)
                #Retrieving the probability of the prediction
                yhat_prob_facenet512 = model_facenet512.predict_proba(facenet512_emb)
                #print("4. Predicting class and probability done")
                class_index_facenet512 = yhat_class_facenet512[0]
    
                class_probability_facenet512 = yhat_prob_facenet512[0,class_index_facenet512] * 100
    
                print('Prediction Probablity of facenet512:%.3f' %(class_probability_facenet512))
    
                tuple_index=(class_index_vggface, class_index_facenet, class_index_facenet512)
                final_pred =mode(tuple_index)
                name=person_rep[final_pred]
                directory="Validation_set/"
                #for name in os.listdir(directory):
                print("\nclass:",name)
                
                class_name=directory+name+'/'
                for face in os.listdir(class_name):
                    face1=class_name+face
                    print("\nface:",face)
                    img = cv2.imread(face1)
                    facenet_emb1=embedding_facenet(cv2.resize(img,(160,160)))
                    cos_dist=findCosineDistance(facenet_emb[0],facenet_emb1[0])
                    print("\ncosinedist",class_name,":",cos_dist)
                    if(cos_dist>0.50):
                        count+=1
                prob=count/10
                print("\nProbability:",prob)
                    
                        
                if(prob>0.6):
                    cv2.putText(frame,"Unknown",(x, y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
                   # cv2.putText(frame,"Unknown",(bounding_box[0], bounding_box[1]-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
               
                   
                else:
                    cv2.putText(frame,person_rep[final_pred],(x, y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
                    #cv2.putText(frame,person_rep[final_pred],(bounding_box[0], bounding_box[1]-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
               
                    
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) &0xFF == ord('q'):
            break
    #When everything's done, release capture
    cap.release()
    cv2.destroyAllWindows()
