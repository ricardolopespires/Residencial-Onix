import decimal
from django.db.models import Avg, Count, Sum ,F, Q
from django.shortcuts import get_object_or_404
from financeiro.models import  Inadimplência
from moradores.models import Morador
from datetime import datetime
from decimal import Decimal
from datetime import date





def calculo_de_vencimento_diario(datetime, date, date_objects, ):
    
    data_atual = date.today()

    for inadimplencia in Inadimplência.objects.filter(Q(status__startswith = 'atrasado')|Q(status__startswith = 'inadinplente')):
   
   
        morador = get_object_or_404(Morador, unidade = inadimplencia.unidade )
        data_atual = date.today()
        inicial = inadimplencia.vencimento.strftime('%d-%m-%Y') 
        final = data_atual.strftime('%d-%m-%Y')
                
        # Data inicial
        d1 = datetime.strptime(inicial, '%d-%m-%Y')       

        # Data final
        d2 =  datetime.strptime(final, '%d-%m-%Y')    

        # Realizamos o calculo da quantidade de dias
        quantidade_dias = abs((d1 - d2).days)
        
        
        condicao_atual = quantidade_dias -(quantidade_dias *2)

        juros = int(quantidade_dias) * float(0.11)
       
        



        if condicao_atual <= -20 or quantidade_dias > -21:

                inadimplencia.juros = Decimal(quantidade_dias) * Decimal(0.11)
                inadimplencia.dias = quantidade_dias
                inadimplencia.valor_total =  Decimal(inadimplencia.boleto) + Decimal(inadimplencia.multa) + Decimal(inadimplencia.juros) + Decimal(inadimplencia.atualizacao)
                inadimplencia.save()


        elif condicao_atual == -21:
                inadimplencia.juros = Decimal(quantidade_dias) * Decimal(0.11)
                inadimplencia.status = "inadimplente"
                inadimplencia.save()
     


