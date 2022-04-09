from datetime import datetime, timedelta
from datetime import date
import random
import sys, os 
import pandas as pd
import json



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Onix.settings")

import django
django.setup()


from financeiro.models import Banco, Conta, Despesas, Movimentacao, Saldo_Anterior, Prazo, Inadimplência
from condominio.models import Condominios, Taxa_Extraordinaria, Taxa_Ordinaria, Ocorrencias
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count, Sum ,F
from accounts.models import Administradores
from moradores.models import Morador
from financeiro.models import Banco, Conta
from boleto.models import Boleto
from django.db.models import Q
from decimal import Decimal




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


    print(juros)
    print(condicao_atual)



    if condicao_atual <= -20 or quantidade_dias > -21:
        print("adicionou o juro diario")
        inadimplencia.juros = Decimal(quantidade_dias) * Decimal(0.11)
        inadimplencia.dias = condicao_atual
        inadimplencia.save()


    elif qcondicao_atual == -21:
        inadimplencia.juros + Decimal(0.11)
        inadimplencia.status = "inadimplente"
        inadimplencia.save()
   

 


        
 
     
            

           

 
                

 
                
    









            
