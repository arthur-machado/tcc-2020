#importa o python-firebase
from firebase import firebase

#configuracao do firebase
firebase =  firebase.FirebaseApplication("https://tcc2020-78c46.firebaseio.com/", None)
#instancia de autenticacao

#defini classes para post's nas tabelas
def InsertUser(name, email, password):
    data = {
        'Name': name,
        'Email': email,
        'Password': password
    }
    result = firebase.post('/tcc2020-78c46/Users', data)
    return result
    
def Login(email, password):
    login = auth.sign_in_with_email_and_password(email, password)