def initFirebase():
    import firebase_admin
    from firebase_admin import credentials

    cred = credentials.Certificate('Dependencies/FirebaseConfig/face-rec-6c441-firebase-adminsdk-h7le5-2ba894b505.json')
    
    firebase_admin.initialize_app(cred, 
    {
        'databaseURL': 'https://Face-rec.firebaseio.com/'
    })