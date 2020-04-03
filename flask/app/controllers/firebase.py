#importa os metodos
from firebase import firebase
from flask import jsonify, make_response, request, redirect


#configuracao do firebase
firebase =  firebase.FirebaseApplication("https://tcc2020-78c46.firebaseio.com/", None)

#defini classes para post's nas tabelas
class user():
    def InsertUser(name, email, password):
        data = {
            'Name': name,
            'Email': email,
            'Password': password
        }
        result = firebase.post('/tcc2020-78c46/Users', data)
        return result

    def Login(email, password):
        authentication = firebase.authentication('THIS_IS_MY_SECRET', email, password)
        firebase.authentication = authentication

        user = authentication.get_user()

        result = firebase.get('/tcc2020-78c46/Users', None)
        print(result)
        return redirect('/meuspets')
      