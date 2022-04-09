from decimal import Decimal
from django.shortcuts import get_object_or_404



def calculo_entre_datas(datas, datetime, date, relativedelta):
    for data in datas:        
        data_inicial = str(date.today())+" 23:59:59" 
        data_final = str(data.data_vencimento) +" 23:59:59" 
        f = "%Y-%m-%d %H:%M:%S"
        inicio = datetime.strptime(data_inicial, f)
        fim = datetime.strptime(data_final, f)
        di = abs(relativedelta(inicio, fim))

        return di    






def mes_restrazado(today, Despesas,):
    data_atual = '0{}/{}'.format(today.month, today.year)
    month = today.month


    try:
        despesas_mes_retrazado = Despesas.objects.filter(vencimento__month = month - 2) 
        uantidade_mes_retrazado = Despesas.objects.filter(vencimento__month = month - 2).count()
            
    except:
        despesas_mes_retrazado = 0
        despesas_mes_passado = 0

    return {
        
        'despesas_mes_retrazado':despesas_mes_retrazado,
        }    




def adicionando_na_inadimplencia(date, datetime, Inadimplência, Boleto, Morador ):
    
    inadimplencia = Inadimplência.objects.all()

    for boleto in Boleto.objects.all():
        boleto

        morador = get_object_or_404(Morador, unidade = boleto.unidade )
        data_atual = date.today()
        inicial = boleto.data_vencimento.strftime('%d-%m-%Y') 
        final = data_atual.strftime('%d-%m-%Y')
            
        # Data inicial
        d1 = datetime.strptime(inicial, '%d-%m-%Y')       

        # Data final
        d2 =  datetime.strptime(final, '%d-%m-%Y')    

        # Realizamos o calculo da quantidade de dias
        quantidade_dias = abs((d1 - d2).days)
        
     

        if d1 < d2:

            condicao_atual = quantidade_dias -(quantidade_dias *2)
            
            print(condicao_atual)

            if Inadimplência.objects.filter(unidade = str(boleto.unidade)).exists() and Inadimplência.objects.filter(vencimento__date = boleto.data_vencimento).exists():
                
                Boleto.objects.filter(unidade = morador.unidade).delete()        

    
            elif condicao_atual >= -2:

                identificador = "INADI" + str(boleto.unidade)+ str(boleto.data_vencimento.strftime('%d%m%Y'))
                id = identificador
                unidade = boleto.unidade
                acordo = False
                status = "atrasado"
                morador_id = morador.id
                vencimento = boleto.data_vencimento
                referente = boleto.data_vencimento
                dias = quantidade_dias
                boleto = Decimal(boleto.valor_documento)
                multa = boleto * Decimal(0.02)
                juros = Decimal(0.11)                
                atualizacao = 0
                honorarios = boleto * Decimal(0.10)
                valor_total = boleto + multa + juros + atualizacao + honorarios
                    
            
                Inadimplência.objects.all().create(

                    id = id,
                    unidade = unidade,
                    acordo = acordo,
                    status = status,
                    morador_id = morador_id,
                    vencimento = vencimento,
                    referente = referente,
                    dias = dias,
                    boleto = boleto,
                    multa = multa,
                    juros = juros,               
                    atualizacao = atualizacao,
                    honorarios = honorarios,
                    valor_total = valor_total,

                    )  
           


            
        

    




def porcentagem(valor_anterior, valor_atual):
    porcetagem = 100
    try:
        calculo = porcetagem / int(valor_anterior)
    except:
        calculo = porcetagem / 1
    resultado =  calculo * valor_atual 
    return float("{0:.2f}".format(resultado))