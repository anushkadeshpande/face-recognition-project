from os import listdir
from os.path import isdir
from numpy import savez_compressed
from numpy import asarray
from mtcnn.mtcnn import MTCNN
import cv2
trainPath = 'Datasets/Train'
testPath = 'Datasets/Test'
# extract a single face from a given photograph
def extract_face(filename, required_size):
    # reading image
    image = cv2.imread(filename)
    # convert to RGB since cv2 read as BGR
    # face size should be 160*160 as per FaceNet model
    face_array = cv2.resize(image,(required_size))
    return face_array

# load images and extract faces for all images in a directory
def load_faces(required_size, directory):
    faces = list()
    # enumerate files
    for filename in listdir(directory):
        # path
        path = directory + filename
        # get face
        face = extract_face(path, required_size)
        # store
        faces.append(face)
    return faces

# load a dataset that contains one subdir for each class that in turn contains images
def load_dataset(required_size, directory):
    X, y = list(), list()
    # enumerate folders, on per class
    for subdir in listdir(directory):
        # path
        path = directory + subdir + '/'
        # skip any files that might be in the dir
        if not isdir(path):
            continue
        # load all faces in the subdirectory
        faces = load_faces(required_size, path)
        # create labels
        labels = [subdir for _ in range(len(faces))]
        # summarize progress
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        # store
        X.extend(faces)
        y.extend(labels)
    return asarray(X), asarray(y)

def dataPreparation(required_size, saveAs):
    # load train dataset
    trainX, trainy = load_dataset(required_size, trainPath+'/')
    print(trainX.shape, trainy.shape)
    # load test dataset
    testX, testy = load_dataset(required_size, testPath+'/')
    # save arrays to one file in compressed format
    savez_compressed(saveAs, trainX, trainy, testX, testy)