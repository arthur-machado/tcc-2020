#adiciona aspas duplas
def TransformationRequest(request):
    #para selecinar dados no JSON, o dicionário vindo do firebase precisa estar em aspas duplas
    #transforma o dict em str
    requeststr = (""" %s """ % (request))
    #passa as aspas duplas para simples
    result = requeststr.replace("'", '"')
    #retorna o resultado
    return result