def dlib_resnet_embeddings():  
        from numpy import load
        from numpy import expand_dims
        from numpy import asarray
        from numpy import savez_compressed
        import tensorflow as tf
        import dlib
        import numpy as np  

        def get_embedding(model, face_pixels):
                img=model.compute_face_descriptor(face_pixels)
                img_representation=np.array(img)
                return img_representation 

        # load the face dataset
        data = load('Backend/Core/Generations/face_detection_dlib.npz')
        trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
        print('Loaded: ', trainX.shape, trainy.shape, testX.shape, testy.shape)
        facerec = dlib.face_recognition_model_v1("Backend/Core/Dependencies/dlib_face_recognition_resnet_model_v1.dat")
        print('Model Loaded dlib')
        # convert each face in the train set to an embedding
        newTrainX = list()
        for face_pixels in trainX:
                embedding = get_embedding(facerec, face_pixels)
                newTrainX.append(embedding)
        newTrainX = asarray(newTrainX)
        print(newTrainX.shape)
        # convert each face in the test set to an embedding
        newTestX = list()
        for face_pixels in testX:
                embedding = get_embedding(facerec, face_pixels)
                newTestX.append(embedding)
        newTestX = asarray(newTestX)
        print(newTestX.shape)
        # save arrays to one file in compressed format
        savez_compressed('Backend/Core/Generations/embeddings/faces-embeddings_dlib_resnet.npz', newTrainX, trainy, newTestX, testy)
