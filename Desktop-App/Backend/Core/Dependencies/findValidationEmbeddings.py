import numpy as np
import cv2
import os
import dlib
val_dlib = []
def find_embedding(model,feature_model, img):    
        if model == "facenet" or model == "facenet512":
            face_pixels = img.astype('float32')
            mean, std = face_pixels.mean(), face_pixels.std()
            face_pixels = (face_pixels - mean) / std
            img = np.expand_dims(face_pixels, axis=0)
        elif model == "arcface":
            img = img.astype(np.float32) / 255.
            if len(img.shape) == 3:
                img = np.expand_dims(img, 0)    
        else:
            img = np.expand_dims(img, axis=0)
        yhat = feature_model.predict(img)
        return yhat

def embedding_dlib(img):
        #face_pixels = img.astype('float32')
        #mean, std = face_pixels.mean(), face_pixels.std()
        #face_pixels = (face_pixels - mean) / std
        model_dlib = dlib.face_recognition_model_v1("Backend/Core/Dependencies/dlib_face_recognition_resnet_model_v1.dat")
        img=model_dlib.compute_face_descriptor(img)
        img_representation=np.array(img)
        return img_representation 

def calculateEmbeddings(model_feature, val, model_name):
    i = 0
    if model_name == "vggface":
        size = (224, 224)
    
    elif model_name == "arcface":
        size = (112, 112)

    else:
        size = (160, 160)

    for person in os.listdir("Datasets/Validation"):
        for img in os.listdir("Datasets/Validation/"+person):
            face1="Datasets/Validation/"+person+'/'+img
            face = cv2.imread(face1)
            if i == 0:
                val_emb = np.array(find_embedding(model_name, model_feature, cv2.resize(face,size)))
                i = 1
            
            else:
                #print(face1)
                val_emb = np.append(val_emb, find_embedding(model_name, model_feature, cv2.resize(face,size)), axis=0)
                
    np.save('Backend/Core/Generations/ValidationEmbeddings/'+ val, val_emb)

def findValidationEmbeddings(model):
    global val_dlib
    from keras.models import Model
    from keras.models import load_model
    
    
    if(model == 'vggface'):
        vggface=load_model('Backend/Core/Generations/models/feature_extractor_model.h5')
        model_feature_vggface=Model(inputs=vggface.layers[0].input,outputs=vggface.layers[-2].output)
        calculateEmbeddings(model_feature_vggface, "val_vgg", "vggface")
    
    elif model == 'facenet':
        model_feature_facenet=load_model('Backend/Core/Generations/models/feature_extractor_model_facenet.h5')
        calculateEmbeddings(model_feature_facenet, "val_facenet", "facenet")

    elif model == 'dlib_resnet':
        #model_feature_dlib_resnet = dlib.face_recognition_model_v1("Backend/Core/Dependencies/dlib_face_recognition_resnet_model_v1.dat")
        #calculateEmbeddings(model_feature_dlib_resnet, "val_dlib_resnet", "dlib_resnet")
        for person in os.listdir("Datasets/Validation"):
            for img in os.listdir("Datasets/Validation/"+person):
                face1="Datasets/Validation/"+person+'/'+img
                face = cv2.imread(face1)
                val_dlib.append(embedding_dlib(cv2.resize(face,(150,150))))
        np.save('Backend/Core/Generations/ValidationEmbeddings/val_dlib_resnet', val_dlib)
    
    elif model == 'arcface':
        model_feature_arcface=load_model('Backend/Core/Generations/models/feature_extractor_model_arcface.h5')
        calculateEmbeddings(model_feature_arcface, "val_arcface", "arcface")
        

    else:
        model_feature_facenet512=load_model('Backend/Core/Generations/models/feature_extractor_model_facenet_512.h5')
        calculateEmbeddings(model_feature_facenet512, "val_facenet_512", "facenet512")
    