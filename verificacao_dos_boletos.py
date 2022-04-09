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
from decimal import Decimal


unidades = []


inadimplencia = Inadimplência.objects.all()

for boleto in Boleto.objects.all():
   
    print(boleto)
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
    print(quantidade_dias)
     
    if d1 < d2:
        condicao_atual = quantidade_dias -(quantidade_dias *2)

 
        if condicao_atual == -1:
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
          juros = boleto * Decimal(0.011)                
          atualizacao = 0
          honorarios = boleto * Decimal(0.10)
          valor_total = boleto + multa + juros + atualizacao + honorarios

         
          if Inadimplência.objects.filter(unidade = str(boleto.unidade)).exists()and Inadimplência.objects.filter(vencimento__date = boleto.data_vencimento).exists():

              Boleto.objects.filter(unidade = morador.unidade).delete()
            
          else :    
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

        
 
        elif Inadimplência.objects.filter(unidade = str(boleto.unidade)).exists()and Inadimplência.objects.filter(vencimento__date = boleto.data_vencimento).exists():

            

           

            for inadimplencia in Inadimplência.objects.all():

                if condicao_atual <= -20 or quantidade_dias > -21:

                    inadimplencia.juros + Decimal(0.11)
                    dias = condicao_atual
                    inadimplencia.save()


                elif qcondicao_atual == -21:
                    inadimplencia.juros + Decimal(0.11)
                    inadimplencia.status = "inadimplente"
                    inadimplencia.save()

                

 
    print('O Boleto está em dia, ainda falta {0} dias'.format(quantidade_dias))
                
    









            
