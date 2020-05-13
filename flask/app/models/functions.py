from datetime import date

#adiciona aspas duplas
def TransformationRequest(request):
    #para selecinar dados no JSON, o dicionário vindo do firebase precisa estar em aspas duplas
    #transforma o dict em str
    requeststr = (""" %s """ % (request))
    #passa as aspas duplas para simples
    result = requeststr.replace("'", '"')
    #retorna o resultado
    return result

#troca dois pontos por underline, possibilitando assim reconhecer a 'chave primária'
def TransformationHour(hour):
    #passa os dois pontos para underline
    result = hour.replace(":", '_')
    #retorna o resultado
    return result



#pega o data atual
def CurrentDate():
    #registra a data atual
    register_date = date.today()
    #grava a data, no forma de string, no formato usado na base dados
    current_date = register_date.strftime('%d_%m_%Y')
    return current_date

