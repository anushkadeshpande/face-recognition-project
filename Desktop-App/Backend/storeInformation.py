def storeInformation(name, address, phone, email):
    import firebase_admin
    from firebase_admin import credentials, firestore
    import datetime

    if not firebase_admin._apps:    
        cred = credentials.Certificate('Dependencies/FirebaseConfig/face-recognition-29af2-firebase-adminsdk-3ligi-448a117215.json')
    
        firebase_admin.initialize_app(cred, 
        {
            'databaseURL': 'https://Face-rec.firebaseio.com/'
        })
    
    db = firestore.client()
    
    doc_ref = db.collection(u'Users')
    # Import data
    
    doc_ref.add({
        'name' : name,
        'address' : address,
        'phone' : phone,
        'email' : email
    })
    
    

    ######### FOR ADDING UNKNOWN PEOPLE

    '''
    import firebase_admin
    from firebase_admin import credentials, firestore
    import datetime
    cred = credentials.Certificate('./face-rec-6c441-firebase-adminsdk-h7le5-2ba894b505.json')
    from firebase_admin import credentials, initialize_app, storage
    # Init firebase with your credentials
    cred = credentials.Certificate('./face-rec-6c441-firebase-adminsdk-h7le5-2ba894b505.json')
    initialize_app(cred, {'databaseURL': 'https://Face-rec.firebaseio.com/','storageBucket': 'face-rec-6c441.appspot.com'})
    db = firestore.client()
    # Put your local file path 
    fileName = "./test1.jpg"
    bucket = storage.bucket()
    blob = bucket.blob('/Unknown People/test1.jpg')
    blob.upload_from_filename(fileName)

    # Opt : if you want to make public access from the URL
    blob.make_public()

    print("your file url", blob.public_url)

    doc_ref = db.collection(u'Logs')
    # Import data
    doc_ref.add({
        'Picture' : blob.public_url,
        'Notified' : False,
        'Time' : datetime.datetime.utcnow()
    })
    '''