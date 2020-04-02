import pyrebase

config = {
    "apiKey": "AIzaSyCDvWv2912C2QyUslTfKhK1xUIl5kWdD4U",
    "authDomain": "tcc2020-78c46.firebaseapp.com",
    "databaseURL": "https://tcc2020-78c46.firebaseio.com",
    "projectId": "tcc2020-78c46",
    "storageBucket": "tcc2020-78c46.appspot.com",
    "messagingSenderId": "978880649824",
    "appId": "1:978880649824:web:b4062a835f23c56b188105",
    "measurementId": "G-E0XTQ7F2LS"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

