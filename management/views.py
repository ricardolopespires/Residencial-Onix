from django.core import exceptions
from django.db.models.expressions import Exists
from financeiro.models import Banco, Conta, Despesas, Inadimplência, Pagamento
from .core import calculo_entre_datas, porcentagem, adicionando_na_inadimplencia
from django.views.generic import View, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from financeiro.core import calculo_de_vencimento_diario
from dateutil.relativedelta import relativedelta
from django.db.models import Avg, Count, Sum ,F
from django.http import HttpResponseRedirect
from accounts.models import Administradores
from condominio.models import Condominios
from boleto.core import gerador_de_boleto
from moradores.models import Morador
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from boleto.models import Boleto
from django.db.models import Q
from datetime import datetime
from datetime import date
from decimal import Decimal

today = date.today()



# Create your views here.
class Management_View_Manager(LoginRequiredMixin, View):

    def get(self, request):
        today = date.today() 
        month = today.month
        condominios = Condominios.objects.all()
        moradores = Morador.objects.all().order_by('unidade') 
        
        adicionando_na_inadimplencia(date, datetime, Inadimplência, Boleto, Morador )

        calculo_de_vencimento_diario(datetime, date, Inadimplência )


        #-------------------------------------- Receitas -----------------------------------------------------------------------------------------------------------------------------------------------       
        
        receitas = Pagamento.objects.filter(data_vencimento__month = month)

    
        try:
            receitas_paga = float(receitas.aggregate(total = Sum('valor_total'))['total'])
        except:
            receitas_paga = 0


      
        try:
            receitas_valor_total = float(condominios.aggregate(total = Sum(F('lancamento_futuro') + F('receitas') + F('inadinplencia')))['total'])

        except:
            receitas_valor_total = 0

        try:
            calculo_valor_total = float('{0:.2f}'.format(condominios.aggregate(total = Sum(F('caixa') + F('inadinplencia') + F('lancamento_futuro') - F('despesas')))['total']))

        except:
            calculo_valor_total  = 0
         
        
        porcentagem_receitas = int(porcentagem(receitas_valor_total,receitas_paga ))
        
              
        #-------------------------------------- Despesas -----------------------------------------------------------------------------------------------------------------------------------------------       
    
        despesas = Despesas.objects.filter(pagamento__month = month)

        try:
            despesas_total = Despesas.objects.filter(pagamento__month = month).count() 

        except:
            despesas_tota = 0

        try:
            despesas_valor_total =  float(Despesas.objects.filter(pagamento__month = month).aggregate(total = Sum('valor'))['total']) 
        except:
             despesas_valor_total = 0 
        try:
            despesas_aberta = float(despesas.filter(status = 'aberta').aggregate(total = Sum('valor'))['total'])
        except:
            despesas_aberta = 0

        try:           
            despesas_paga = float(despesas.filter(status = 'paga').aggregate(total = Sum('valor'))['total'])
        except:
            despesas_paga = 0

        try:
            despesas_atrasadas = float(despesas.filter(status = 'atrasada').aggregate(total = Sum('valor_total'))['total'])
        except:
            despesas_atrasadas = 0 


        try:
            funcionario = int(despesas.filter(despesas ='funcionario').aggregate(total = Sum('valor'))['total'])
        except:
            funcionario = 0


        calculo_valor_total_despesas = despesas_aberta + despesas_paga + despesas_atrasadas

        try:        
            
            manutencao = int(despesas.filter(despesas = 'manutencao').aggregate(total = Sum('valor'))['total'])
            consumo = int(despesas.filter(despesas = 'consumo').aggregate(total = Sum('valor'))['total'])
            outros = int(despesas.filter(despesas = 'outros').aggregate(total = Sum('valor'))['total'])          
            
        
        except:           
            
            manutencao = 0
            consumo = 0
            outros = 0
        


        
        porcentagem_funcionario = int(porcentagem(despesas_valor_total, funcionario ))
        porcetagem_manutencao = int(porcentagem(despesas_valor_total, manutencao))
        porcentagem_consumo = int(porcentagem(despesas_valor_total, consumo))
        porcentagem_outros = int(porcentagem(despesas_valor_total, outros))
        porcentagem_despesas = int(porcentagem(despesas_valor_total, despesas_paga))       

        porcentagem_calculo = int(porcentagem(receitas_valor_total,despesas_valor_total ))
   
               
       #-------------------------------------- GERADOR DE BOLETO -----------------------------------------------------------------------------------------------------------------------------------------------         

        boletos = Boleto.objects.filter(data_vencimento__month = month).order_by('unidade')
        data_restante = calculo_entre_datas(boletos, datetime, date, relativedelta)            
        total_boletos = Boleto.objects.filter(status = 'aberto').count()
        boletos_pagos = Boleto.objects.filter(status = 'pagos ').count()

       



        if total_boletos > 0 and today.day < 26:            
            lancamentos_futuros = float("{0:.2f}".format( Boleto.objects.filter(Q(status__startswith = 'aberto'),  Q(data_vencimento__month = month)).aggregate(total=Sum('valor_documento'))['total']))
        else:
            lancamentos_futuros = 0        
        

        try:
            inadinplencias = float("{0:.2f}".format(Inadimplência.objects.filter(Q(status__startswith = 'inadinplente') | Q(status__startswith = 'Atrasado')).aggregate(total = Sum('valor_total'))['total']))

        except:
            inadinplencias = 0
        try:
            saldo = float("{0:.2f}".format(Conta.objects.all().aggregate(total = Sum('saldo'))['total']))        
        except:
            saldo = 0
        try:
            caixa = "{0:.2f}".format(condominios.aggregate(total=Sum(F('conta_poupança') + F('conta_corrente')))['total'],)
        except:
            caixa = 0
                           
        condominios.update(
            
            conta_corrente = saldo,
            caixa = caixa,
            receitas = receitas_paga,
            despesas = despesas_valor_total,            
            lancamento_futuro = lancamentos_futuros,
            inadinplencia = inadinplencias,
        )

        month = '{}'.format(today.month)                
        dia = '{}'.format(today.day)

        boleto = Boleto.objects.filter(status__startswith = 'aberto').count()
        print(boleto)     
        
        if dia == '27' and Boleto.objects.all().count() == 0:
            gerador_de_boleto(Condominios, Morador, Administradores, date, datetime, Boleto)
            messages.success(request, "Os boletos do que vem foram gerados con sucesso")
                




         #-------------------------------------- CONTA BANCARIA -----------------------------------------------------------------------------------------------------------------------------------------------       

        conta_corrente = Conta.objects.filter(tipo = 'conta corrente')
        conta_poupanca = Conta.objects.filter(tipo = 'poupança')

        dia = '{}'.format(today.day)
        
        if dia == '1':
            for corrente in conta_corrente:
                corrente.debitos = 0        
                corrente.creditos = 0
                corrente.creditos = corrente.saldo
                corrente.save()

        

        #conta_corrente.update(saldo = conta_corrente.aggregate(total = Sum(F('creditos') - F('debitos')))['total'])
        #conta_poupanca.update(saldo = conta_poupanca.aggregate(total = Sum(F('creditos') - F('debitos')))['total'])
        
        return render(request, 'management/manager.html',{
            
            'despesas_valor_total':despesas_valor_total,'receitas_paga':receitas_paga,'receitas':receitas,            
            'porcentagem_receitas':porcentagem_receitas,'condominios':condominios,'lancamentos_futuros':lancamentos_futuros,
            'moradores':moradores,'month':month,'boletos':boletos,'data_restante':data_restante,'funcionario':funcionario,
            'porcentagem_funcionario': porcentagem_funcionario,'manutencao':manutencao,'porcetagem_manutencao':porcetagem_manutencao,
            'consumo':consumo,'porcentagem_consumo':porcentagem_consumo,'outros':outros,'porcentagem_outros':porcentagem_outros,
            'despesas':despesas,'receitas_valor_total':receitas_valor_total,'porcentagem_despesas':porcentagem_despesas,
            'despesas_aberta':despesas_aberta,'despesas_paga':despesas_paga,'despesas_atrasadas':despesas_atrasadas,'calculo_valor_total':calculo_valor_total,
            'porcentagem_calculo':porcentagem_calculo,'calculo_valor_total_despesas':calculo_valor_total_despesas,
           
            
            })
            







