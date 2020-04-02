#importa o Pyrebase4
import pyrebase

#configuracao do firebase
configFirebase = {
    "apiKey": "AIzaSyCDvWv2912C2QyUslTfKhK1xUIl5kWdD4U",
    "authDomain": "tcc2020-78c46.firebaseapp.com",
    "databaseURL": "https://tcc2020-78c46.firebaseio.com",
    "projectId": "tcc2020-78c46",
    "storageBucket": "tcc2020-78c46.appspot.com",
    "messagingSenderId": "978880649824",
    "appId": "1:978880649824:web:b4062a835f23c56b188105",
    "measurementId": "G-E0XTQ7F2LS"
}

#inicializa o firebase
firebase =  pyrebase.initialize_app(configFirebase)
#instancia de autenticacao
auth = firebase.auth()
#instancia para o real time database
db = firebase.database()
#defini uma chave secreta para a sessao
#app.secret_key = os.urandom(24)
