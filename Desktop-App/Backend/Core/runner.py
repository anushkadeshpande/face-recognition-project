from dataPreparation import dataPreparation

# SAVE MODELS
from vgg16_rec2 import vgg16
from facenet128 import facenet128
from facenet512 import facenet512

from facenet_embeddings import facenet_embeddings
from facenet_embeddings_512 import facenet_512_embeddings
from vggface_embeddings import vggface_embeddings
    
# CLASSIFICATION
from classification import classification

from findValidationEmbeddings import findValidationEmbeddings

def vggface():
    dataPreparation((224, 224), "Backend/Core/Generations/face_detection_vggface.npz")
    vgg16()
    vggface_embeddings()
    classification('Backend/Core/Generations/embeddings/faces-embeddings_vggface.npz', 'Backend/Core/Generations/classifierModels/finalized_model_vggface.sav', 'Backend/Core/Generations/predLabels/vggface_predicted_labels.npz')
    findValidationEmbeddings("vggface")

def facenet():
    dataPreparation((160, 160), "Backend/Core/Generations/face_detection.npz")
    facenet128()
    facenet_embeddings()
    classification('Backend/Core/Generations/embeddings/faces-embeddings.npz', 'Backend/Core/Generations/classifierModels/finalized_model.sav', 'Backend/Core/Generations/predLabels/facenet_predicted_labels.npz')
    findValidationEmbeddings("facenet")

def facenet_512():
    dataPreparation((160, 160), "Backend/Core/Generations/face_detection_512.npz")
    facenet512()
    facenet_512_embeddings()
    classification('Backend/Core/Generations/embeddings/faces-embeddings_512.npz', 'Backend/Core/Generations/classifierModels/finalized_model_512.sav', 'Backend/Core/Generations/predLabels/facenet512_predicted_labels.npz')
    findValidationEmbeddings("facenet512")


def runner():
    import os
    trainPath = 'Datasets/Train'
    testPath = 'Datasets/Test'
    if not os.path.exists('Backend/Core/Generations'):
        os.makedirs('Backend/Core/Generations')
    
    if not os.path.exists('Backend/Core/Generations/embeddings'):
        os.makedirs('Backend/Core/Generations/embeddings')
    if not os.path.exists('Backend/Core/Generations/classifierModels'):
        os.makedirs('Backend/Core/Generations/classifierModels')
    
    if not os.path.exists('Backend/Core/Generations/ValidationEmbeddings'):
        os.makedirs('Backend/Core/Generations/ValidationEmbeddings')

    from multiprocessing import Process
    from threading import Thread
    
    process_1 = Thread(target=vggface())
    process_2 = Thread(target=facenet())
    process_3 = Thread(target=facenet_512())
    process_1.start()
    process_2.start()
    process_3.start()
     
