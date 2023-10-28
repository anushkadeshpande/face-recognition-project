
def arcface_embeddings(): 
    # calculate a face embedding for each face in the dataset using arcface
    from numpy import load
    from numpy import expand_dims
    from numpy import asarray
    from numpy import savez_compressed
    from tensorflow.keras.models import load_model
    from tensorflow.keras.models import Model
    import tensorflow as tf
    import numpy as np
    import cv2
    from keras.preprocessing import image

    with tf. device("cpu:0"):
    # get the face embedding for one face


        def get_embedding(model, img):
            img = img.astype(np.float32) / 255.
            if len(img.shape) == 3:
                img = np.expand_dims(img, 0)
            yhat = model.predict(img)
            return yhat[0]


        # load the face dataset
        data = load('Backend/Core/Generations/face_detection_arcface.npz')
        trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
        print('Loaded: ', trainX.shape, trainy.shape, testX.shape, testy.shape)
        # load the facenet model
        arcface = load_model('Backend/Core/Generations/models/feature_extractor_model_arcface.h5')
    
        print('Model Loaded arcface')
        # convert each face in the train set to an embedding
        newTrainX = list()
        for face_pixels in trainX:
                embedding = get_embedding(arcface, face_pixels)
                #print("\n\nEmebdding",embedding)
                newTrainX.append(embedding)
        newTrainX = asarray(newTrainX)
        print(newTrainX.shape)
        # convert each face in the test set to an embedding
        newTestX = list()
        for face_pixels in testX:
                embedding = get_embedding(arcface, face_pixels)
                #print("\nEmbedding shape",embedding.shape)
                newTestX.append(embedding)
        newTestX = asarray(newTestX)
        print(newTestX.shape)
        # save arrays to one file in compressed format
        savez_compressed('Backend/Core/Generations/embeddings/faces-embeddings_arcface.npz',
                            newTrainX, trainy, newTestX, testy)
