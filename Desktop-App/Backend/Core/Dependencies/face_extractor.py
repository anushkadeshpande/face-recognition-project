def face_extractor(img):
    import cv2
    import os

    face_classifier = cv2.CascadeClassifier('Dependencies/haarcascade_frontalface_default.xml')
    
    faces = face_classifier.detectMultiScale(img, 1.3, 5)
    
    if faces == ():
        return None
    
    for (x,y,w,h) in faces:
        h=h+15
        y=y-10
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face

    