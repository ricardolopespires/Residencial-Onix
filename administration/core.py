



from datetime import date


def calculo_entre_datas(inicial, termino, datetime, relativedelta):

    data_inicial = str(inicial)[:-7]   
    data_final = str(termino) [:-7] 
    data_atual = str(date.today())+ " 00:00:0"
    
    f = "%Y-%m-%d %H:%M:%S"
    hoje = datetime.strptime(data_atual, f)
    inicio = datetime.strptime(data_inicial, f)
    fim = datetime.strptime(data_final, f)
    
    #di = abs(relativedelta(inicio, fim))
   
    tempo_total = fim - inicio
    tempo_parcial = fim - hoje


    return {'tempo_total':tempo_total.days, 'tempo_parcial':tempo_parcial.days}  







def procetagem_diaria(valor_anterior, valor_atual):

    porcetagem = 100
    calculo = int(porcetagem) / int(valor_anterior)
    resultado = valor_atual * calculo
    return float("{0:.2f}".format(resultado))