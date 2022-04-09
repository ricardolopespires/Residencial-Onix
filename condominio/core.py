from datetime import datetime, timedelta
from datetime import date
import sys, os 
import pandas as pd
import json


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Onix.settings")

import django
django.setup()




def calculo_de_data_ocorrencias(datetime, Ocorrencias):
    for ocorrencia in Ocorrencias.objects.all():
        
        data = ocorrencia.created.strftime('%d-%m-%Y')

        # Data inicial
        d1 = datetime.strptime(data, '%d-%m-%Y')
        
        # Data final
        d2 =  d1 +  timedelta(days = 2)   
        # Realizamos o calculo da quantidade de dias
        quantidade_dias = abs((d2 - d1).days)         
        ocorrencia.dias = quantidade_dias
        ocorrencia.save()
        resultado =  quantidade_dias + 20
        return resultado



def calculo_diferenca_de_data(datetime, object_de_entrada):
    
    
    for data in object_de_entrada.objects.all():
        
        inicial = data.inicio.strftime('%d-%m-%Y')
        final = data.termino.strftime('%d-%m-%Y')

        # Data inicial
        d1 = datetime.strptime(inicial, '%d-%m-%Y')       
        # Data final
        d2 =  datetime.strptime(final, '%d-%m-%Y')    
        # Realizamos o calculo da quantidade de dias
        quantidade_dias = abs((d1 - d2).days)
        return quantidade_dias 




def calculo_diferenca_da_data_atual(datetime, object_de_entrada):
    
    data_atual = datetime.now()

    for data in object_de_entrada.objects.all():
        
        inicial = data_atual.strftime('%d-%m-%Y')
        final = data.termino.strftime('%d-%m-%Y')

        # Data inicial
        d1 = datetime.strptime(inicial, '%d-%m-%Y')       
        # Data final
        d2 =  datetime.strptime(final, '%d-%m-%Y')    
        # Realizamos o calculo da quantidade de dias
        quantidade_dias = abs((d1 - d2).days)
        return quantidade_dias 



def porcentagem(valor_anterior, valor_atual):
    porcetagem = 100
    calculo = int(porcetagem) / int(valor_anterior)
    resultado = valor_atual * calculo
    return float("{0:.2f}".format(resultado))