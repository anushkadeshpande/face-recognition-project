def logUnknown(picNum):
    import firebase_admin
    from firebase_admin import credentials, firestore, initialize_app, storage
    import datetime
    import os
    import requests
    # Init firebase with your credentials
    if not firebase_admin._apps:
        print("Initializing firebase")
        cred = credentials.Certificate('Dependencies/FirebaseConfig/face-recognition-29af2-firebase-adminsdk-3ligi-448a117215.json')
        initialize_app(cred, {'databaseURL': 'https://Face-rec.firebaseio.com/','storageBucket': 'face-recognition-29af2.appspot.com'})
    
    db = firestore.client()
    # Put your local file path 
 
    for picName in os.listdir('./Capture'):
        if picName[0] != 'n': 
            fileName = "./Capture/"+picName
            bucket = storage.bucket()
            blob = bucket.blob('/Unknown People/'+picName)
            blob.upload_from_filename(fileName)

            # Opt : if you want to make public access from the URL
            blob.make_public()

            print("your file url", blob.public_url)

            doc_ref = db.collection(u'Logs')
            # Import data
            doc_ref.add({
                'Picture' : blob.public_url,
                'Time' : datetime.datetime.utcnow()
            })

            data = {
                "app_id": "0a807065-20b8-4c43-a875-50bc94fd049f",
                "included_segments": ["All"],
                "headings" : {"en": "Alert"},
                "contents": {"en": "Unknown Person detected!"},
                "big_picture" : blob.public_url
            }


            requests.post(
                "https://onesignal.com/api/v1/notifications",
                headers={"Authorization": "Basic MzdmZjNmZDYtNmIxZC00M2E4LTkxMjctZThkMjA3ODRkZjg1"},
                json=data
            )

            os.rename('./Capture/'+picName, './Capture/n'+picName)
        #os.remove("./Capture/"+img_name[0])

