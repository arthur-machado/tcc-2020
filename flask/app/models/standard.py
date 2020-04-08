#metodo que 'padroniza' o id em codigo ascii dos caracteres
def StandardId(id):
    soma_ascii = 0
    for x in id:
        #pega cada caractere do id recebido do firebase e soma, gerando assim outro id
        soma_ascii+=ord(x)
    return soma_ascii