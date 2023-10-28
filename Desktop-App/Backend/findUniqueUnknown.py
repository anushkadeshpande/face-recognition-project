
def find_embedding(img):    
    import numpy as np
    from keras.models import load_model

    model_feature_facenet512=load_model('Backend/Core/Generations/models/feature_extractor_model_facenet_512.h5')
  
    face_pixels = img.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    sample_img = np.expand_dims(face_pixels, axis=0)

    yhat = model_feature_facenet512.predict(sample_img)
    return yhat

def findUniqueUnknown(unknown_emb, newUnknown):
    import os
    import cv2
    from findCosineDistance import findCosineDistance

    newUnknown_emb = find_embedding(cv2.resize(newUnknown, (160,160)))
    for emb in unknown_emb:
        #face = cv2.imread('./Capture/'+img)
        #print(img)
        #val_emb = find_embedding(cv2.resize(face,(160,160)))
        cos_dist=findCosineDistance(newUnknown_emb[0],emb[0])
        if(cos_dist<0.3):
            return 0

    if len(os.listdir('./Capture')) == 5:
        print("Removing 1st photo")
        os.remove('./Capture/'+os.listdir('./Capture')[0])
        unknown_emb.pop(0)
        unknown_emb.append(newUnknown_emb)
    return unknown_emb
        
            