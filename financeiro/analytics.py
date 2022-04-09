





def porcentagem(valor_anterior, valor_atual):
    porcetagem = 100
    try:
        calculo = porcetagem / int(valor_anterior)
    except:
        calculo = porcetagem / 1
    resultado =  calculo * valor_atual 
    return float("{0:.2f}".format(resultado))