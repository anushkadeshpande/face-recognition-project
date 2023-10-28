# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 02:47:21 2022

@author: Anushka
"""
def classification(dataPath, file, predLabelFile):
    global cosineDistance
    import os
    import numpy as np
    from numpy import load
    from sklearn.metrics import accuracy_score
    from sklearn.preprocessing import LabelEncoder
    from sklearn.preprocessing import Normalizer
    from sklearn.svm import SVC
    from numpy import savez_compressed
    import pickle
    # load dataset
    # embedding data
    data = load(dataPath)
    trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    print('Dataset: train=%d, test=%d' % (trainX.shape[0], testX.shape[0]))
    # normalize input vectors
    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)
    testX = in_encoder.transform(testX)
    # label encode targets
    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    trainy = out_encoder.transform(trainy)
    testy = out_encoder.transform(testy)
    # fit model
    model = SVC(kernel='linear',C=1, probability=True)
    model.fit(trainX, trainy)
    #Saving Model
    filename = file
    pickle.dump(model, open(filename, 'wb'))
    # predict
    yhat_train = model.predict(trainX)
    yhat_test = model.predict(testX)
    # save arrays to one file in compressed format
    if not os.path.exists('Backend/Core/Generations/predLabels'):
        os.makedirs('Backend/Core/Generations/predLabels')

    savez_compressed(predLabelFile, yhat_train, yhat_test)
    # score
    score_train = accuracy_score(trainy, yhat_train)
    score_test = accuracy_score(testy, yhat_test)
    # summarize
    print('Accuracy: train=%.3f, test=%.3f' % (score_train*100, score_test*100))
    
    