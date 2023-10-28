import multiprocessing
from threading import Thread
def dataPrepThread():
    from dataPreparation import dataPreparation
    process_1 = Thread(target=dataPreparation((160, 160), "Backend/Core/Generations/face_detection.npz"))
    ##process_2 = Thread(target=dataPreparation((160, 160), "Backend/Core/Generations/face_detection_512.npz"))
    process_2 = Thread(target=dataPreparation((150, 150), "Backend/Core/Generations/face_detection_dlib.npz"))
    process_3 = Thread(target=dataPreparation((224, 224), "Backend/Core/Generations/face_detection_vggface.npz"))
    process_4 = Thread(target=dataPreparation((112, 112), "Backend/Core/Generations/face_detection_arcface.npz"))
    process_1.start()
    process_2.start()
    process_3.start()
    process_4.start()
    #process_1.join()
    #process_2.join()
    #process_3.join()

def classificationThread():
    from classification import classification
    process_1 = Thread(target=classification('Backend/Core/Generations/embeddings/faces-embeddings_vggface.npz', 'Backend/Core/Generations/classifierModels/finalized_model_vggface.sav', 'Backend/Core/Generations/predLabels/vggface_predicted_labels.npz'))
    process_2 = Thread(target=classification('Backend/Core/Generations/embeddings/faces-embeddings.npz', 'Backend/Core/Generations/classifierModels/finalized_model.sav', 'Backend/Core/Generations/predLabels/facenet_predicted_labels.npz'))
    process_3 = Thread(target=classification('Backend/Core/Generations/embeddings/faces-embeddings_512.npz', 'Backend/Core/Generations/classifierModels/finalized_model_512.sav', 'Backend/Core/Generations/predLabels/facenet512_predicted_labels.npz'))
    process_4 = Thread(target=classification('Backend/Core/Generations/embeddings/faces-embeddings_dlib_resnet.npz', 'Backend/Core/Generations/classifierModels/finalized_model_dlib_resnet.sav', 'Backend/Core/Generations/predLabels/dlib_resnet_predicted_labels.npz'))
    process_5 = Thread(target=classification('Backend/Core/Generations/embeddings/faces-embeddings_arcface.npz', 'Backend/Core/Generations/classifierModels/finalized_model_arcface.sav', 'Backend/Core/Generations/predLabels/arcface_predicted_labels.npz'))
    
    process_1.start()
    process_2.start()
    process_3.start()
    process_4.start()
    process_5.start()
    #process_1.join() 2:39 started training
    #process_2.join()
    #process_3.join()

def runner():
    import os
    trainPath = 'Datasets/Train'
    testPath = 'Datasets/Test'
    if not os.path.exists('Backend/Core/Generations'):
        os.makedirs('Backend/Core/Generations')

    '''
    # DATA PREPARATION
    from dataPreparation import dataPreparation
    
    dataPreparation((160, 160), "Backend/Core/Generations/face_detection.npz")
    dataPreparation((160, 160), "Backend/Core/Generations/face_detection_512.npz")
    dataPreparation((224, 224), "Backend/Core/Generations/face_detection_vggface.npz")
    '''

    dataPrepThread()
    
    # SAVE MODELS
    from saveModels import saveModels
    
    saveModels()
    
    
    # PREPARE EMBEDDINGS
    from prepareEmbeddings import PrepareEmbeddings
    
    PrepareEmbeddings()
    
    
    # CLASSIFICATION
    from classification import classification
    if not os.path.exists('Backend/Core/Generations/classifierModels'):
        os.makedirs('Backend/Core/Generations/classifierModels')
    '''
    classification('Backend/Core/Generations/embeddings/faces-embeddings_vggface.npz', 'Backend/Core/Generations/classifierModels/finalized_model_vggface.sav')
    classification('Backend/Core/Generations/embeddings/faces-embeddings.npz', 'Backend/Core/Generations/classifierModels/finalized_model.sav')
    classification('Backend/Core/Generations/embeddings/faces-embeddings_512.npz', 'Backend/Core/Generations/classifierModels/finalized_model_512.sav')
    '''
    classificationThread()
    
    from findValidationEmbeddings import findValidationEmbeddings
    if not os.path.exists('Backend/Core/Generations/ValidationEmbeddings'):
        os.makedirs('Backend/Core/Generations/ValidationEmbeddings')

    findValidationEmbeddings("vggface")
    findValidationEmbeddings("facenet")
    findValidationEmbeddings("facenet512")
    findValidationEmbeddings("dlib_resnet")
    findValidationEmbeddings("arcface")