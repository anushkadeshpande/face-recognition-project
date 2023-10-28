# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 22:05:21 2022

@author: Bhavini
"""
import pandas as pd
from numpy import load
from statistics import mode
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import asarray
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
labels_vggface = load('Generations/predLabels/vggface_predicted_labels.npz')
yhat_train_vggface, yhat_test_vggface = labels_vggface['arr_0'], labels_vggface['arr_1']


labels_facenet = load('Generations/predLabels/facenet_predicted_labels.npz')
yhat_train_facenet, yhat_test_facenet = labels_facenet['arr_0'], labels_facenet['arr_1']



labels_facenet512 = load('Generations/predLabels/facenet512_predicted_labels.npz')
yhat_train_facenet512, yhat_test_facenet512 = labels_facenet512['arr_0'], labels_facenet512['arr_1']

data = load('Generations/face_detection_vggface.npz')
testy = data['arr_3']

predictions = pd.DataFrame(columns=['vggface',
                                    'facenet',
                                    'facenet512'])
predictions['vggface'] = yhat_test_vggface
predictions['facenet'] = yhat_test_facenet
predictions['facenet512'] = yhat_test_facenet512

# Lets take a look at the end of the dataframe
yhat_test_facenet512
predictions.head()
predictions

final_predictions = []
for preds in predictions.iterrows():
    final_predictions.append(mode(preds[1].values))
   
final_predictions=asarray(final_predictions)
final_predictions

out_encoder = LabelEncoder()
out_encoder.fit(testy)
testy = out_encoder.transform(testy)
testy
def plt_conf_mat(y_true, y_pred, title):
    # Plotting confusion matrix
    
    plt.figure(figsize=(8,6))
    sns.heatmap(confusion_matrix(y_true, y_pred),
                annot=True,
                square=True)
    plt.xlabel('Predicted Class')
    plt.ylabel('Original Class')
    plt.title("{} Confusion Matrix".format(title))
    plt.show()
plt_conf_mat(testy, final_predictions, 'Max Voting')
testy
final_predictions
score_test=accuracy_score(testy, final_predictions)
print('Accuracy:%.3f' % ( score_test*100))
print('Classification Report')
print('='*50)
print(classification_report(testy, final_predictions))