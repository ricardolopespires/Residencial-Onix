






def calculo_entre_datas(datas, datetime, date, relativedelta):
    for data in datas:        
        data_inicial = str(date.today())+" 23:59:59" 
        data_final = str(data.data_vencimento) +" 23:59:59" 
        f = "%Y-%m-%d %H:%M:%S"
        inicio = datetime.strptime(data_inicial, f)
        fim = datetime.strptime(data_final, f)
        di = abs(relativedelta(inicio, fim))

        return di    






def porcentagem(valor_anterior, valor_atual):
    porcetagem = 100
    try:
        calculo = porcetagem / int(valor_anterior)
    except:
        calculo = porcetagem / 1
    resultado =  calculo * valor_atual 
    return float("{0:.2f}".format(resultado))