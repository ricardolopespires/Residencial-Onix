from financeiro.models import Banco, Conta, Despesas, Inadimplência, Pagamento
from django.views.generic import View, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from dateutil.relativedelta import relativedelta
from django.db.models import Avg, Count, Sum ,F, Q
from django.http import HttpResponseRedirect
from condominio.models import Condominios
from .core import calculo_entre_datas
from moradores.models import Morador
from datetime import datetime, date
from django.contrib import messages
from boleto.models import Boleto
from django.urls import reverse
from .core import porcentagem
from django.db import models
from decimal import Decimal
from datetime import date






today = date.today()



class Dashboard_View(LoginRequiredMixin,View):


    def get(self, request):
        
        today = date.today() 
        month = today.month
        condominios = Condominios.objects.all()
        moradores = Morador.objects.all().order_by('unidade') 



    #----------------------------------------- Receitas Mês Passado ---------------------------------------------------------------------------------
       

        try:
            receitas_valor_total_mes_passado = float(Pagamento.objects.filter(data_vencimento__month = month - 1).aggregate(total = Sum('valor_total'))['total'])

        except:
            receitas_valor_total_mes_passado = 0

       


     
    #-------------------------------------- Despesas Mês Passado -----------------------------------------------------------------------------------------------------
    
       
        try:
            despesas_valor_total_mes_passado =  float(Despesas.objects.filter(pagamento__month = month-1).aggregate(total = Sum('valor'))['total']) 
        except:
             despesas_valor_total_mes_passado = 0 

        total_caixa_mes_passado = float(receitas_valor_total_mes_passado - despesas_valor_total_mes_passado)

   
    #-------------------------------------- Inadimplências Mês Passado --------------------------------------------------------------------------------------------------
        try:
            total_inadinplencias_mes_passado =  float('{0:.2f}'.format(Inadimplência.objects.filter(vencimento__month = month - 1).aggregate(total = Sum(('valor_total')))['total']))
        except:
            total_inadinplencias_mes_passado = 0

      

    #-------------------------------------- Receitas Mês Atual ----------------------------------------------------------------------------------------------------------
        
        receitas = Pagamento.objects.filter(data_vencimento__month = month)

        try:
            receitas_paga = float(receitas.aggregate(total = Sum('valor_total'))['total'])
        except:
            receitas_paga = 0

        try:
            total_receita_mes_atual = float(condominios.aggregate(total = Sum(F('lancamento_futuro') + F('receitas') + F('inadinplencia')))['total'])

        except:
            total_receita_mes_atual = 0

        try:
            calculo_total_despesas_abertas = float('{0:.2f}'.format(Despesas.objects.filter(status = 'aberta').aggregate(total = Sum('valor'))['total']))
        except:
            calculo_total_despesas_abertas = 0

        try:
            calculo_valor_total = float('{0:.2f}'.format(condominios.aggregate(total = Sum(F('caixa') + F('receitas') + F('inadinplencia') - F('despesas')))['total']))

        except:
            calculo_valor_total  = 0

        #-------------------------------------- Inadimplências Mês Atual --------------------------------------------------------------------------------------------------
        try:
            total_inadinplencias_mes_atual =  float('{0:.2f}'.format(Inadimplência.objects.filter(vencimento__month = month ).aggregate(total = Sum(('valor_total')))['total']))
        except:
            total_inadinplencias_mes_atual = 0
        
        porcentagem_total_receitas_mes_atual = int(porcentagem(total_receita_mes_atual,receitas_paga ))
        
    
        
        

        #-------------------------------------- Despesas Mês Atual -----------------------------------------------------------------------------------------------------------------------------------------------       
    
        despesas = Despesas.objects.filter(pagamento__month = month)

        try:
            despesas_total = Despesas.objects.filter(pagamento__month = month).count() 

        except:
            despesas_tota = 0

        try:
            despesas_valor_total_mes_atual =  float(Despesas.objects.filter(pagamento__month = month).aggregate(total = Sum('valor'))['total']) 
        except:
             despesas_valor_total_mes_atual = 0 
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
        


        
        porcentagem_funcionario = int(porcentagem(despesas_valor_total_mes_atual, funcionario ))
        porcetagem_manutencao = int(porcentagem(despesas_valor_total_mes_atual, manutencao))
        porcentagem_consumo = int(porcentagem(despesas_valor_total_mes_atual, consumo))
        porcentagem_outros = int(porcentagem(despesas_valor_total_mes_atual, outros))
        porcentagem_despesas = int(porcentagem(despesas_valor_total_mes_atual, despesas_paga))       

        porcentagem_calculo = int(porcentagem(total_receita_mes_atual, despesas_valor_total_mes_atual ))



   
   
               
       #-------------------------------------- Mês Atual -----------------------------------------------------------------------------------------------------------------------------------------------         

        boletos = Boleto.objects.filter(data_vencimento__month = month).order_by('unidade')
        data_restante = calculo_entre_datas(boletos, datetime, date, relativedelta)            
        total_boletos = Boleto.objects.filter(status = 'aberto').count()
        boletos_pagos = Boleto.objects.filter(status = 'pagos ').count()

        if total_boletos > 0: 
            try:
                lancamentos_futuros = float( Boleto.objects.filter(Q(status__startswith = 'aberto'), Q(data_vencimento__month = month)).aggregate(total=Sum('valor_documento'))['total'])
            except:
                lancamentos_futuros = 0

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
            total_caixa_mes_atual = float("{0:.2f}".format(condominios.aggregate(total=Sum(F('conta_poupança') + F('conta_corrente')))['total'],))
        except:
            total_caixa_mes_atual = 0
                           
        condominios.update(
            
            conta_corrente = saldo,
            caixa = total_caixa_mes_atual,
            despesas = despesas_valor_total_mes_atual,            
            lancamento_futuro = lancamentos_futuros,
            inadinplencia = inadinplencias,
        )

        porcetagem_total_receita_mes_atual =  float("{0:.2f}".format(porcentagem(receitas_valor_total_mes_passado, total_receita_mes_atual)))
        procentagem_total_caixa_mes_atual =  float("{0:.2f}".format(porcentagem(total_caixa_mes_passado, total_caixa_mes_atual)))
        porcentagem_total_despesas_mes_atual = float("{0:.2f}".format(porcentagem(despesas_valor_total_mes_passado, despesas_valor_total_mes_atual)))
        total_porcentagem_inadinplencias_mes_atual = porcentagem(total_inadinplencias_mes_passado, total_inadinplencias_mes_atual)

        
 
        #-------------------------------------- CONTA BANCARIA -----------------------------------------------------------------------------------------------------------------------------------------------       

        conta_corrente = Conta.objects.filter(tipo = 'conta corrente')
        conta_poupanca = Conta.objects.filter(tipo = 'poupança')
        conta_corrente.update(saldo = conta_corrente.aggregate(total = Sum(F('creditos') - F('debitos')))['total'])
        conta_poupanca.update(saldo = conta_poupanca.aggregate(total = Sum(F('creditos') - F('debitos')))['total'])
        
        return render(request, 'dashboard/manager.html',{
            
            'despesas_valor_total_mes_atual':despesas_valor_total_mes_atual,'receitas_paga':receitas_paga,'receitas':receitas,            
            'porcentagem_total_receitas_mes_atual':porcentagem_total_receitas_mes_atual,'condominios':condominios,'lancamentos_futuros':lancamentos_futuros,
            'moradores':moradores,'month':month,'boletos':boletos,'data_restante':data_restante,'funcionario':funcionario,
            'porcentagem_funcionario': porcentagem_funcionario,'manutencao':manutencao,'porcetagem_manutencao':porcetagem_manutencao,
            'consumo':consumo,'porcentagem_consumo':porcentagem_consumo,'outros':outros,'porcentagem_outros':porcentagem_outros,
            'despesas':despesas,'total_receita_mes_atual':total_receita_mes_atual,'porcentagem_despesas':porcentagem_despesas,
            'despesas_aberta':despesas_aberta,'despesas_paga':despesas_paga,'despesas_atrasadas':despesas_atrasadas,'calculo_valor_total':calculo_valor_total,
            'porcentagem_calculo':porcentagem_calculo,'calculo_valor_total_despesas':calculo_valor_total_despesas,'total_caixa_mes_atual':total_caixa_mes_atual,
            'inadinplencias':inadinplencias,'total_caixa_mes_passado':total_caixa_mes_passado,'procentagem_total_caixa_mes_atual':procentagem_total_caixa_mes_atual ,
            'porcetagem_total_receita_mes_atual':porcetagem_total_receita_mes_atual,'receitas_valor_total_mes_passado':receitas_valor_total_mes_passado,
            'porcentagem_total_despesas_mes_atual':porcentagem_total_despesas_mes_atual, 'despesas_valor_total_mes_passado':despesas_valor_total_mes_passado,
            'total_porcentagem_inadinplencias_mes_atual':total_porcentagem_inadinplencias_mes_atual,'total_inadinplencias_mes_atual':total_inadinplencias_mes_atual,
            'total_inadinplencias_mes_passado':total_inadinplencias_mes_passado,


            
           
            
            })
        
      

class Financeiro_View(LoginRequiredMixin,View):


    def get(self, request , id_unidade):
        today = date.today()
        data_atual = '0{}/{}'.format(today.month, today.year)

        morador = get_object_or_404(Morador,unidade = id_unidade)

        inadimplencias = Inadimplência.objects.filter(unidade__startswith = morador.unidade).order_by('referente')

        try:
            total_inadinplencias = float("{0:.2f}".format(Inadimplência.objects.filter(Q(unidade__startswith = morador.unidade), Q(status__startswith = 'inadinplente') | Q(status__startswith = 'Atrasado')).aggregate(total = Sum('valor_total'))['total']))

        except:
            total_inadinplencias = 0

        boletos = Boleto.objects.filter(unidade = morador.unidade)        
   

        valor_total =float("{0:.2f}".format(Decimal(morador.valor_total) + Decimal(total_inadinplencias)))
        
        return render(request,'dashboard/financeiro/index.html',{
            
            'data_atual':data_atual, 'morador':morador,'total_inadinplencias':total_inadinplencias, 'valor_total':valor_total,
            'boletos':boletos,'inadimplencias':inadimplencias,
            
            })



class Ocorrencia(LoginRequiredMixin, View):

    def get(self, request, id_unidade):
        
        today = date.today()
        data_atual = '0{}/{}'.format(today.month, today.year)

        morador = get_object_or_404(Morador,unidade = id_unidade)

        return render(request, 'dashboard/ocorrencia/index.html',{'data_atual':data_atual, 'morador':morador, })