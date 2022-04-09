from management.core import mes_restrazado
from .forms import BancoForm, ContasForm, Despesas_Mensal_Form, Movimentacao_Form, Deposito_Form
from .models import Banco, Conta, Despesas, Movimentacao, Pagamento, Saldo_Anterior, Prazo, Inadimplência
from django.views.generic import View, TemplateView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Sum ,F, Q
from .models import Categoria,  SubCategoria
from django.http import HttpResponseRedirect
from accounts.models import Administradores
from condominio.models import Condominios
from moradores.models import Morador
from .analytics import porcentagem
from django.contrib import messages
from django.urls import reverse
from random import randint
from datetime import date
from decimal import Decimal
import random
today = date.today()



# Create your views here.


#--------------------------------------- CONTABILIDADE -----------------------------------------------------

class Contabilidade_Manager(LoginRequiredMixin, View):

    def get(self, request):
        month = today.month
        condominios = Condominios.objects.all()
        despesas = Despesas.objects.filter(pagamento__month = month).order_by('vencimento')
        valor_total_despesas = despesas.aggregate(total = Sum('valor_total'))['total']
        receitas = Pagamento.objects.filter(data_vencimento__month = month).order_by('data_pagamento')
        return render(request, 'financeiro/contabilidade/contabil.html', {
            
            'condominios':condominios,'despesas':despesas,'receitas':receitas,'valor_total_despesas':valor_total_despesas,
            
            })



class Multas_View(View):

    def get(self, request):
        return render(request, 'financeiro/contabilidade/multas.html')




class Inadimplencia_Mes_Anterior_View(LoginRequiredMixin, View):

    def get(self, request):
       
        if today.month < 10:
            data_atual = '0{}/{}'.format(today.month -1, today.year)
        else:
            data_atual = '{}/{}'.format(today.month -1, today.year) 


            
        month = today.month -1
        total_unidades = Morador.objects.count()

               #-----------------------------Mês Retrasado --------------------------------------------------------------------------------------------
        
        inadinplencias_mes_retrasado = Inadimplência.objects.filter(vencimento__month = month - 2) 
        unidades_mes_retrasado = inadinplencias_mes_retrasado.count()        
        try:
            total_mes_retrasado = float("{0:.2f}".format(inadinplencias_mes_retrasado.aggregate(total = Sum(F('valor_total') ))['total']))
        except:
            total_mes_retrasado = 0
        
        try:
            total_juros_mes_retrasado = float("{0:.2f}".format(inadinplencias_mes_retrasado.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
            total_juros_mes_retrasado = 0

        porcetagem_total_mes_retrasado = porcentagem(0, total_mes_retrasado)
        porcentagem_unidade_mes_retrasado = porcentagem(total_unidades, unidades_mes_retrasado)       
        porcetagem_juros_mes_retrasado = porcentagem(0, total_juros_mes_retrasado )        
        porcentagem_porcentagem_unidade_mes_retrasado = porcentagem(0, porcentagem_unidade_mes_retrasado)       
        

        #-----------------------------Mês Anterior --------------------------------------------------------------------------------------------
        
        inadinplencias_mes_passado = Inadimplência.objects.filter(vencimento__month = month - 1)

        try:
            total_unidades_mes_passado = inadinplencias_mes_passado.count()        
        except:
            total_unidades_mes_atual = 0
        try:
            total_mes_passado = float("{0:.2f}".format(inadinplencias_mes_passado.aggregate(total = Sum(F('valor_total') ))['total']))
        except:
            total_mes_passado = 0
        
        try:
            total_juros_mes_passado = float("{0:.2f}".format(inadinplencias_mes_passado.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
            total_juros_mes_passado = 0

        porcetagem_total_mes_passado = porcentagem(total_mes_retrasado, total_mes_passado)
        porcentagem_total_unidades_mes_passado = porcentagem(total_unidades, total_unidades_mes_passado )       
        porcetagem_total_juros_mes_passado = porcentagem(total_juros_mes_retrasado, total_juros_mes_passado )        
        porcentagem_porcentagem_unidade_mes_passado = porcentagem(porcentagem_unidade_mes_retrasado, porcentagem_total_unidades_mes_passado)
        #------------------------------ Mês Atual ---------------------------------------------------------------------------------------------
        
        

        inadinplencias_mes_atual = Inadimplência.objects.filter(vencimento__month = month)

        try:
            total_mes_autal = float("{0:.2f}".format(inadinplencias_mes_atual.aggregate(total = Sum(F('valor_total') ))['total']))
        except:
            total_mes_autal = 0

        
        try:
            total_unidades_mes_atual = inadinplencias_mes_atual.count() 
        except:
            total_unidades_mes_atual = 0
       

        try:
            total_juros_mes_atual = float("{0:.2f}".format(inadinplencias_mes_atual.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
            total_juros_mes_atual = 0            
      

        porcetagem_total_mes_atual = porcentagem(total_mes_autal, total_mes_passado)
        porcetagem_total_juros_mes_atual = porcentagem(total_juros_mes_atual , total_juros_mes_passado)
        porcentagem_total_unidade_mes_atual = porcentagem(total_unidades_mes_atual, total_unidades_mes_passado )
        porcentagem_unidade_total = porcentagem(total_unidades, total_unidades_mes_atual)
        porcentagem_porcentagem_unidade_mes_atual = porcentagem(porcentagem_unidade_total, porcentagem_total_unidades_mes_passado)
     


        return render(request, 'financeiro/inadinplentes/mes_anterior.html',{

            'data_atual':data_atual ,'total_mes_passado':total_mes_passado, 'porcetagem_total_mes_passado':porcetagem_total_mes_passado,'porcetagem_total_juros_mes_passado':porcetagem_total_juros_mes_passado, 
            'porcentagem_porcentagem_unidade_mes_passado': porcentagem_porcentagem_unidade_mes_passado,'porcentagem_total_unidades_mes_passado':porcentagem_total_unidades_mes_passado,
            'total_unidades_mes_passado':total_unidades_mes_passado,'total_juros_mes_passado':total_juros_mes_passado,

            'inadinplencias_mes_atual':inadinplencias_mes_atual,'total_mes_autal':total_mes_autal,'porcetagem_total_mes_atual':porcetagem_total_mes_atual, 
            'total_unidades_mes_atual': total_unidades_mes_atual,  'porcentagem_total_unidade_mes_atual':porcentagem_total_unidade_mes_atual,
            'total_juros_mes_atual':total_juros_mes_atual, 'porcetagem_total_juros_mes_atual': porcetagem_total_juros_mes_atual,'porcentagem_unidade_total':porcentagem_unidade_total,
            'porcentagem_porcentagem_unidade_mes_atual': porcentagem_porcentagem_unidade_mes_atual,
            
            
            })

            

class Inadimplencia_Mes_Atual_View(LoginRequiredMixin, View):

    def get(self, request):
           
        if today.month < 10:
            data_atual = '0{}/{}'.format(today.month, today.year)
        else:
            data_atual = '{}/{}'.format(today.month, today.year) 
    
                  
        month = today.month


        total_unidades = Morador.objects.count()

         #-----------------------------Mês Retrasado --------------------------------------------------------------------------------------------
        
        inadinplencias_mes_retrasado = Inadimplência.objects.filter(vencimento__month = month - 2) 
        unidades_mes_retrasado = inadinplencias_mes_retrasado.count()        
        try:
            total_mes_retrasado = float("{0:.2f}".format(inadinplencias_mes_retrasado.aggregate(total = Sum(F('valor_total') ))['total']))
        except:
            total_mes_retrasado = 0
        
        try:
            total_juros_mes_retrasado = float("{0:.2f}".format(inadinplencias_mes_retrasado.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
            total_juros_mes_retrasado = 0

        porcetagem_total_mes_retrasado = porcentagem(0, total_mes_retrasado)
        porcentagem_unidade_mes_retrasado = porcentagem(total_unidades, unidades_mes_retrasado)       
        porcetagem_juros_mes_retrasado = porcentagem(0, total_juros_mes_retrasado )        
        porcentagem_porcentagem_unidade_mes_retrasado = porcentagem(0, porcentagem_unidade_mes_retrasado)       
        

        #-----------------------------Mês Anterior --------------------------------------------------------------------------------------------
        
        inadinplencias_mes_passado = Inadimplência.objects.filter(vencimento__month = month - 1)

        try:
            total_unidades_mes_passado = inadinplencias_mes_passado.count()        
        except:
            total_unidades_mes_atual = 0
        try:
            total_mes_passado = float("{0:.2f}".format(inadinplencias_mes_passado.aggregate(total = Sum(F('valor_total') ))['total']))
        except:
            total_mes_passado = 0
        
        try:
            total_juros_mes_passado = float("{0:.2f}".format(inadinplencias_mes_passado.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
            total_juros_mes_passado = 0

        porcetagem_total_mes_passado = porcentagem(total_mes_retrasado, total_mes_passado)
        porcentagem_total_unidades_mes_passado = porcentagem(total_unidades, total_unidades_mes_passado )       
        porcetagem_total_juros_mes_passado = porcentagem(total_juros_mes_retrasado, total_juros_mes_passado )        
        porcentagem_porcentagem_unidade_mes_passado = porcentagem(porcentagem_unidade_mes_retrasado, porcentagem_total_unidades_mes_passado)
        #------------------------------ Mês Atual ---------------------------------------------------------------------------------------------
        
        inadinplencias_mes_atual = Inadimplência.objects.filter(vencimento__month = month)

        try:
            total_mes_atual = float("{0:.2f}".format(inadinplencias_mes_atual.aggregate(total = Sum(F('valor_total') ))['total']))
        except:
            total_mes_atual = 0

        
        try:
            total_unidades_mes_atual = inadinplencias_mes_atual.count() 
        except:
            total_unidades_mes_atual = 0
       

        try:
            total_juros_mes_atual = float("{0:.2f}".format(inadinplencias_mes_atual.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
            total_juros_mes_atual = 0            
      

        porcetagem_total_mes_atual = porcentagem(total_mes_atual, total_mes_passado)
        porcetagem_total_juros_mes_atual = porcentagem(total_juros_mes_atual ,total_juros_mes_passado)
        porcentagem_total_unidade_mes_atual = porcentagem(total_unidades_mes_atual ,total_unidades_mes_passado, )
        porcentagem_unidade_total = porcentagem(total_unidades, total_unidades_mes_atual)
        porcentagem_porcentagem_unidade_mes_atual = porcentagem( porcentagem_unidade_total, porcentagem_total_unidades_mes_passado,)

      

        return render(request, 'financeiro/inadinplentes/mes_atual.html',{

            'data_atual':data_atual ,'total_mes_passado':total_mes_passado, 'porcetagem_total_mes_passado':porcetagem_total_mes_passado,'porcetagem_total_juros_mes_passado':porcetagem_total_juros_mes_passado, 
            'porcentagem_porcentagem_unidade_mes_passado': porcentagem_porcentagem_unidade_mes_passado,'porcentagem_total_unidades_mes_passado':porcentagem_total_unidades_mes_passado,
            'total_unidades_mes_passado':total_unidades_mes_passado,'total_juros_mes_passado':total_juros_mes_passado,

            'inadinplencias_mes_atual':inadinplencias_mes_atual,'total_mes_atual':total_mes_atual,'porcetagem_total_mes_atual':porcetagem_total_mes_atual, 
            'total_unidades_mes_atual': total_unidades_mes_atual,  'porcentagem_total_unidade_mes_atual':porcentagem_total_unidade_mes_atual,
            'total_juros_mes_atual':total_juros_mes_atual, 'porcetagem_total_juros_mes_atual': porcetagem_total_juros_mes_atual,'porcentagem_unidade_total':porcentagem_unidade_total,
            'porcentagem_porcentagem_unidade_mes_atual': porcentagem_porcentagem_unidade_mes_atual,
            
            
            })



class Inadimplencia_Ano_Passado_View(LoginRequiredMixin, View):

    def get(self, request):
        year = today.year -1
        moradores = Morador.objects.count()

        #-----------------------------Ano Retrasado --------------------------------------------------------------------------------------------
        inadinplencias_year_before = Inadimplência.objects.filter(vencimento__year = year - 2).order_by('referente')
        try:
            unidades_year_before = inadinplencias_year_before.count()              
        except:
            unidades_year_before = 0
        try:
            total_year_before = float("{0:.2f}".format(inadinplencias_year_before.aggregate(total = Sum(F('valor_total') ))['total']))
        except:
            total_year_before = 3320.62
        try:
            juros_year_before = float("{0:.2f}".format(inadinplencias_year_before.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
            juros_year_before = 0

        #-----------------------------Ano Passando --------------------------------------------------------------------------------------------
        
        inadinplencias_year_anterior = Inadimplência.objects.filter(vencimento__year = year - 1).order_by('referente')
        try:
            unidades_anteriores = inadinplencias_year_anterior.count()              
        except:
            unidades_anteriores = 0
        try:
            total_year_anterior = float("{0:.2f}".format(inadinplencias_year_anterior.aggregate(total = Sum(F('valor_total') ))['total']))
        except:
            total_year_anterior = 3320.62
        try:
            juros_year_anterior = float("{0:.2f}".format(inadinplencias_year_anterior.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
            juros_year_anterior = 0
        
        porcentagem_unidade_before = porcentagem(unidades_year_before, unidades_anteriores)
        porcentagem_juros_year_before = float("{0:.2f}".format(porcentagem(juros_year_before  ,juros_year_anterior)))
       
        #------------------------------ Mês Atual ---------------------------------------------------------------------------------------------
       
        inadinplencias = Inadimplência.objects.filter(vencimento__year = year).order_by('referente')
        try:
            unidades_autal = inadinplencias.count()
        except:
            unidades_autal = 0
        condominios = Condominios.objects.all()
        try:
            valor_total_mes_atual = float("{0:.2f}".format(inadinplencias.aggregate(total = Sum(F('valor_total') ))['total']))        
        except:
            valor_total_mes_atual = 0
        try:
            juros_year_atual = float("{0:.2f}".format(inadinplencias.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
            juros_year_atual = 0 
        
        condominios.update(inadinplencia = valor_total_mes_atual)

        try:
            porcentagem_valor_total_anteriores = porcentagem(total_year_anterior, valor_total_mes_atual)
        except:
            porcentagem_valor_total_anteriores = 0

        porcentagem_unidade_anteriores = porcentagem( unidades_autal, unidades_anteriores)
        porcentagem_juros_year = porcentagem(juros_year_atual, juros_year_anterior)
        porcentagem_juros_year_atual = float("{0:.2f}".format(porcentagem(porcentagem_juros_year_before, porcentagem_juros_year)))

        return render(request, 'financeiro/inadinplentes/ano_passado.html',{
            
            'inadinplencias':inadinplencias, 'valor_total_mes_atual':valor_total_mes_atual, 'juros_year_atual':juros_year_atual,
            'year':year,'porcentagem_unidade_anteriores':porcentagem_unidade_anteriores,'porcentagem_valor_total_anteriores':porcentagem_valor_total_anteriores,
            'porcentagem_juros_year':porcentagem_juros_year,'porcentagem_juros_year_atual':porcentagem_juros_year_atual,
            
            
            })
            


class Inadimplencia_Anual_View(LoginRequiredMixin, View):

    def get(self, request):
        year = today.year
        moradores = Morador.objects.count()

        #-----------------------------Ano Retrasado --------------------------------------------------------------------------------------------
        inadinplencias_year_before = Inadimplência.objects.filter(vencimento__year = year - 2).order_by('referente')
        try:
            unidades_year_before = inadinplencias_year_before.count()              
        except:
            unidades_year_before = 0
        try:
            total_year_before = float("{0:.2f}".format(inadinplencias_year_before.aggregate(total = Sum(F('valor_total') ))['total']))
        except:
            total_year_before = 3320.62
        try:
            total_juros_anual_retrassado = float("{0:.2f}".format(inadinplencias_year_before.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
            total_juros_anual_retrassado= 0

        #-----------------------------Ano Passando --------------------------------------------------------------------------------------------
        
        inadinplencias_year_anterior = Inadimplência.objects.filter(vencimento__year = year - 1).order_by('referente')
        try:
            total_unidades_ano_passado = inadinplencias_year_anterior.count()              
        except:
            total_unidades_ano_passado = 0
        try:
           total_valor_anual_passado = float("{0:.2f}".format(inadinplencias_year_anterior.aggregate(total = Sum(F('valor_total') ))['total']))
        except:
            total_valor_anual_passado = 0
        try:
            total_juros_anual_passado = float("{0:.2f}".format(inadinplencias_year_anterior.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
             total_juros_anual_passado = 0
        
        porcentagem_unidade_ano_passado = porcentagem(unidades_year_before, total_unidades_ano_passado)
        porcentagem_juros_ano_passado = float("{0:.2f}".format(porcentagem(total_juros_anual_retrassado , total_juros_anual_passado)))

        #------------------------------ Ano Atual ---------------------------------------------------------------------------------------------
       
        inadinplencias_ano_atual = Inadimplência.objects.filter(vencimento__year = year).order_by('referente')
        total_unidades_ano_autal =  inadinplencias_ano_atual.count()
        condominios = Condominios.objects.all()

        print(total_unidades_ano_autal)

        try:
            total_valor_anual_atual = float("{0:.2f}".format( inadinplencias_ano_atual.aggregate(total = Sum(F('valor_total') ))['total']))    
        except:
            total_valor_anual_atual =  0

        try:
            total_juros_anual_atual = float("{0:.2f}".format(inadinplencias_ano_atual.aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total']))
        except:
             total_juros_anual_atual = 0

        condominios.update(inadinplencia = total_valor_anual_atual )

              
        procentagem_valor_total_anual_atual = float("{0:.2f}".format(porcentagem(total_valor_anual_atual, total_valor_anual_passado )))
        porcentagem_unidade_ano_atual = float("{0:.2f}".format(porcentagem(total_unidades_ano_autal, total_unidades_ano_passado )))
        porcentagem_juros_ano_atual = float("{0:.2f}".format(porcentagem( total_juros_anual_atual, total_juros_anual_passado)))

       

        return render(request, 'financeiro/inadinplentes/anual.html',{

            'inadinplencias_ano_atual':inadinplencias_ano_atual,

            'total_valor_anual_passado':total_valor_anual_passado,' total_unidades_ano_passado ': total_unidades_ano_passado,
            'total_juros_anual_passado':total_juros_anual_passado, 

            'total_valor_anual_atual': total_valor_anual_atual,'procentagem_valor_total_anual_atual':procentagem_valor_total_anual_atual,
            'total_unidades_ano_autal':total_unidades_ano_autal,'porcentagem_unidade_ano_atual':porcentagem_unidade_ano_atual,
            'total_juros_anual_atual': total_juros_anual_atual, 'porcentagem_juros_ano_atual':porcentagem_juros_ano_atual,           

           
            
            })


class Acordos_View(LoginRequiredMixin, View):

        def get(self, request):

            month = today.month

            total_de_acordos_mes_anterior = Inadimplência.objects.filter( Q(status__startswith = 'acordo'), Q(referente__month = month - 1)).count()           
            

            #--------------------------------------------------- Mês Atual----------------------------------
            data_atual = '0{}/{}'.format(today.month, today.year)
            acordos_mes_atual = Inadimplência.objects.filter( status__startswith = 'acordo')
            total_de_acordos = Inadimplência.objects.filter( status__startswith = 'acordo').count()
            try:
                valor_total = "{0:.2f}".format(acordos_mes_atual.aggregate(total = Sum(F('valor_total') ))['total'])
            except:
                valor_total = 0
            try:
                juros_mes_atual = "{0:.2f}".format(acordos_mes_atual .aggregate(total = Sum(F('juros') + F('multa') + F('atualizacao') + F('honorarios') ))['total'])
            except:
                juros_mes_atual = 0        
            porcentagem_mensal = porcentagem(total_de_acordos_mes_anterior, total_de_acordos)
            acordos_mes_atual.update(valor_total = acordos_mes_atual.aggregate(total = Sum(F('boleto') + F('juros') + F('multa') + F('atualizacao') + F('honorarios')))['total'])
            return render(request, 'financeiro/acordos/manager.html',{

                'total_de_acordos':total_de_acordos,'data_atual':data_atual,'acordos_mes_atual':acordos_mes_atual,
                'valor_total':valor_total, 'juros_mes_atual':juros_mes_atual,'porcentagem_mensal':porcentagem_mensal,
                
                
                })




class Created_Acordo(LoginRequiredMixin, View):


    def get(self, request):
        acordos = Inadimplência.objects.filter(Q(status__startswith = 'atrasado') | Q( status__startswith = 'inadimplente'))

        return render(request, 'financeiro/acordos/created.html', {'acordos':acordos})




class Acordo(LoginRequiredMixin, View):

    def post(self, request):

        if request.method == 'POST':
            vencimento = request.POST.get("vencimento")
            print(vencimento)
           
            

            return HttpResponseRedirect(reverse('financeiro:acordo_manager'))



class Juridico_View(View):

    def get(self, request):
        return render(request, 'financeiro/inadinplentes/juridicos.html')





class Boleto_Pagamento(LoginRequiredMixin, View):

    def get(self, request, pk):
        data_atual = date.today()
        inadimplencia = get_object_or_404(Inadimplência, id = pk)
        sacado =get_object_or_404(Morador, unidade = inadimplencia.unidade)
        cedentes = Condominios.objects.all()
        return  render (request, 'financeiro/inadinplentes/pagamento.html', {
            
            'inadimplencia':inadimplencia, 'sacado':sacado, 'cedentes':cedentes,
            'data_atual':data_atual,
            
            })




class Pagamento_View(LoginRequiredMixin, View):


    def post(self, request, pk):
        inadimplencia = get_object_or_404(Inadimplência, id = pk)
        sacado = get_object_or_404(Morador, unidade = inadimplencia.unidade)
        
        print(sacado)
        cedentes = Condominios.objects.all()
        for cedente in cedentes:
            cedente        
    
        # Criar o array 3 x 3 com números aleatórios entre 1 e 52
        numero_ordem = random.randint(0,10000)   

        if request.method == 'POST':           
            data_do_pagamento = request.POST.get('data_do_pagamento')
            multa =  Decimal(request.POST.get('multa'))
            desconto =  Decimal(request.POST.get('desconto'))
            valor_boleto = Decimal(inadimplencia.valor_total)
            taxa_boleto = Decimal(3.93)
            total =  valor_boleto + multa - desconto - taxa_boleto 
            Pagamento.objects.create(

            id = numero_ordem,
            unidade = inadimplencia.unidade,
            morador_id = sacado.id,
            data_vencimento = inadimplencia.vencimento,
            data_pagamento = data_do_pagamento,
            valor_total =  valor_boleto + multa - desconto - taxa_boleto, 
        )

        conta = get_object_or_404(Conta, tipo = 'conta corrente')    

        valor_documento =  Decimal("{0:.2f}".format(valor_boleto - taxa_boleto))
        valor_total  = conta.saldo + Decimal(valor_documento)
       
        
        conta.creditos += valor_documento
        conta.saldo += total
        conta.save()

        Movimentacao.objects.filter(conta = conta).get_or_create(

                    sindico_id = conta.sindico_id,
                    conta = conta,
                    data = date.today(),
                    descricao = 'unidade pagante: ' + str( inadimplencia.unidade),
                    tipo = 'C',
                    valor = valor_boleto + multa - desconto - taxa_boleto ,
                    saldo = valor_total,
                ) 


        inadimplencia.status = 'quitado'
        inadimplencia.save()
        sacado.valor_total = 0
        sacado.save()

        condominio = get_object_or_404(Condominios, nome = cedente)
        condominio
        condominio.receitas += valor_documento
        condominio.save()
                 
        return HttpResponseRedirect(reverse('financeiro:inadinplencias_mes_atual'))

        
#--------------------------------------- MANAGEMENT BANCOS -------------------------------------------------

class Banco_Manager(LoginRequiredMixin, View):

    def get(self, request):
        bancos = Banco.objects.all()
        data_atual = str(date.today())
        
        return render(request, 'financeiro/banco/bancos.html', {'bancos':bancos, 'data_atual':data_atual} )



class Adicionar_Banco(LoginRequiredMixin, View):

    def get(self, request):
        if request.method == 'Get':
            form = BancoForm(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('financeiro:manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = BancoForm()
        return render(request, 'financeiro/banco/adicionar_banco.html',{'form':form})


    def post(self, request):
        if request.method == 'POST':
            form = BancoForm(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('financeiro:manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = BancoForm()
        return render(request, 'financeiro/banco/adicionar_banco.html', {'form':form})
        




class Conta_Manager(LoginRequiredMixin, View):

    def get(self, request, pk):
      conta_corrente = Conta.objects.filter(Q(agencia_id = pk), Q(tipo = 'conta corrente'))
      conta_poupanca = Conta.objects.filter(Q(agencia_id = pk), Q(tipo = 'poupança'))

      #conta_corrente.update(saldo = conta_corrente.aggregate(total = Sum(F('creditos') - F('debitos')))['total'])
      #conta_poupanca.update(saldo = conta_poupanca.aggregate(total = Sum(F('creditos') - F('debitos')))['total'])
      return render(request, 'financeiro/banco/contas.html',{'conta_poupanca': conta_poupanca,'conta_corrente':conta_corrente})


class Extrato_Conta(LoginRequiredMixin, View):

    def get(self, request, pk):

        month = today.month
        print(month)

        conta = get_object_or_404(Conta, id = pk)
        creditos = "{0:.2f}".format(Conta.objects.filter(id = pk).aggregate(total=Sum('creditos'))['total'])
        debitos = "{0:.2f}".format(Conta.objects.filter(id = pk).aggregate(total=Sum('debitos'))['total'])
        saldo_anteriores = Saldo_Anterior.objects.filter(conta = conta) 
        movimentacoes =  Movimentacao.objects.filter(Q(conta = conta), Q(data__month = month))

        conta_corrente = Conta.objects.filter(Q(agencia_id = pk), Q(tipo = 'conta corrente'))
        conta_poupanca = Conta.objects.filter(Q(agencia_id = pk), Q(tipo = 'poupança'))
        
        #conta_corrente.update(saldo = conta_corrente.aggregate(total = Sum(F('creditos') - F('debitos')))['total'])
        #conta_poupanca.update(saldo = conta_poupanca.aggregate(total = Sum(F('creditos') - F('debitos')))['total'])

        return render(request, 'financeiro/banco/extrato.html', {
            
            'conta':conta,'saldo_anteriores':saldo_anteriores, 'debitos':debitos, 
            'creditos':creditos, 'movimentacoes':movimentacoes 
            
            })


class Adicionar_Contas(LoginRequiredMixin, View):

    def get(self, request):        
        bancos = Banco.objects.all()
        condominios = Condominios.objects.all()
        administradores = Administradores.objects.all()
        if request.method == 'Get':
            banco = Banco.objects.filter(id = pk)
            form = ContasForm(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('financeiro:bancos'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = ContasForm()
        return render(request, 'financeiro/banco/adicionar_contas.html',{'form':form , 'bancos':bancos, 'condominios':condominios,'administradores':administradores})


    def post(self, request):
        bancos = Banco.objects.all()
        condominios = Condominios.objects.all()
        administradores = Administradores.objects.all()
        if request.method == 'POST':
            form = ContasForm(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('financeiro:bancos'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = ContasForm()
        return render(request, 'financeiro/banco/adicionar_contas.html', {'form':form,'bancos':bancos, 'condominios':condominios,'administradores':administradores})





class Deposito_View(LoginRequiredMixin, View):



    def get(self, request, conta_id): 
        administradores = Administradores.objects.all()       
        
        if request.method == 'GET':
            form = Deposito_Form()
        return render(request, 'financeiro/banco/deposito.html',{'form':form, 'administradores':administradores})


    def post(self, request, conta_id):
        conta = get_object_or_404(Conta ,id = conta_id)
        contas = Conta.objects.filter(id =  conta_id)
        for cont in contas:
            cont      
        
        if request.method == 'POST':            
            valor = Decimal(request.POST.get('valor'))
            depositante = request.POST.get('sindico')
            tipo = request.POST.get('tipo')
            movimentocao = Movimentacao.objects.filter(conta = conta)
            conta.creditos += valor
            conta.saldo += valor
            conta.save()
            movimentocao.create(

                sindico_id = depositante,
                conta = cont,
                data = date.today(),
                descricao = "Depósito Bancário",
                tipo = "C",
                valor = valor,
                saldo = conta.saldo + valor,

                            )
           
            
            messages.success(request, 'O seu Depósito no Valor de R$'+ str(valor) + ' está confirmado')
            return HttpResponseRedirect(reverse('financeiro:contas',args = [conta.agencia.id]))

            

        else:
            form = Deposito_Form()
        return render(request, 'financeiro/contabilidade/contas/despesas.html',{'form':form, })
        



#--------------------------------------- / MANAGEMENT BANCOS -------------------------------------------------

#--------------------------------------- / MANAGEMENT DESPESAS -------------------------------------------------


class Adicionar_Despesas_Mensal(LoginRequiredMixin, View):

    def get(self, request):        
        categorias = Categoria.objects.all()
        atividades = SubCategoria.objects.all()
        sindicos = Administradores.objects.all()
        prazo = Prazo.objects.all()
        if request.method == 'Get':
            banco = Banco.objects.filter(id = pk)
            form = Despesas_Mensal_Form(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save( commit = False)               
                prazo.create(

                    despesas = form.cleaned_data['id'],
                    title = form.cleaned_data['servico'],
                    descricao = form.cleaned_data['descricao'],
                    status = 0,
                    complete = False,
                    complete_per = 0,
                    due = form.cleaned_data['vencimento'],
                )
                
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados, junto com os Prazos ')
                return HttpResponseRedirect(reverse('financeiro:despesas_manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Despesas_Mensal_Form()
        return render(request, 'financeiro/contabilidade/contas/adicionar.html',{'form':form, 'categorias':categorias, 'atividades':atividades, 'sindicos':sindicos})


    def post(self, request):
        categorias = Categoria.objects.all()
        atividades = SubCategoria.objects.all()
        sindicos = Administradores.objects.all()
        prazo = Prazo.objects.all()
        if request.method == 'POST':
            form = Despesas_Mensal_Form(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save( commit = False)                 
                prazo.create(

                    id = form.cleaned_data['id'],
                    title = form.cleaned_data['servico'],
                    descricao = form.cleaned_data['descricao'],
                    status = 0,
                    complete = False,
                    complete_per = 0,
                    due = form.cleaned_data['vencimento'],
                )
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados, junto com os Prazos ')
                return HttpResponseRedirect(reverse('financeiro:despesas_manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Despesas_Mensal_Form()
        return render(request, 'financeiro/contabilidade/contas/adicionar.html',{'form':form, 'categorias':categorias, 'atividades':atividades, 'sindicos':sindicos})
        


class Despesas_Manager(LoginRequiredMixin, View):

    def get(self, request):
        
        if today.month < 10:
            data_atual = '0{}/{}'.format(today.month, today.year)
        else:
            data_atual = '{}/{}'.format(today.month, today.year)
             
        month = today.month

        total_unidades = Morador.objects.all().count()


        #----------------------------- Mês Retrasado--------------------------------------------------------------------------------------------
        
        
        try:
            despesas_mes_retrasado = Despesas.objects.filter(vencimento__month = month - 2) 
            quantidade_mes_retrasado = despesas_mes_retrasado.count()
            juros_mes_retrasado = float('{0:.2f}'.format(despesas_mes_retrasado.aggregate(total = Sum('multa'))['total']))
            despesas_mes_retrasado_valor_total = float('{0:.2f}'.format(despesas_mes_retrasado.aggregate(total = Sum('valor_total'))['total']))
            
           
        except:
            despesas_mes_retrasado = 0
            despesas_mes_passado = 0
            juros_mes_retrasado = 0
            despesas_mes_retrasado_valor_total = 0
            
            
        
        porcentagem_mes_retrasado = porcentagem( 0 , despesas_mes_retrasado_valor_total)
        porcentagem_quantidade_despesas_mes_retrasado = porcentagem( 0 , quantidade_mes_retrasado)
        porcentagem_juros_mes_retrasado = porcentagem(0 , juros_mes_retrasado)
        porcentagem_porcentagem_mes_restrasado = porcentagem(0 , porcentagem_juros_mes_retrasado)
        
        
        #----------------------------- Mês Passado --------------------------------------------------------------------------------------------
        
        
        try:
            despesas_mes_passado = Despesas.objects.filter(pagamento__month = month - 1) 
            quantidades_mes_passando = despesas_mes_passado .count()
            juros_mes_passado = float('{0:.2f}'.format(despesas_mes_passado.aggregate(total = Sum('multa'))['total']))
            despesas_mes_passado_valor_total = float('{0:.2f}'.format(despesas_mes_passado.aggregate(total = Sum('valor_total'))['total']))

        except:
            despesas_mes_passado = 0
            quantidades_mes_passando = 0
            juros_mes_passado = 0
            despesas_mes_passado_valor_total = 0
     
  
        porcentagem_mes_passado = porcentagem(despesas_mes_retrasado_valor_total, despesas_mes_passado_valor_total)
        porcentagem_quantidades_mes_passando = porcentagem(quantidade_mes_retrasado, quantidades_mes_passando)
        porcentagem_juros_mes_passado = porcentagem(juros_mes_retrasado, juros_mes_passado)
        porcentagem_porcentagem_mes_passado = porcentagem(porcentagem_mes_retrasado, porcentagem_mes_passado)

        #------------------------------ Mês Atual ---------------------------------------------------------------------------------------------
       
        try:
            despesas_mes_atual = Despesas.objects.filter(pagamento__month = month ).order_by('vencimento')       
            quantidades_mes_atual = despesas_mes_atual.count()
            juros_mes_atual = float('{0:.2f}'.format(despesas_mes_atual.aggregate(total = Sum('multa'))['total']))
            despesas_mes_atual_valor_total = float('{0:.2f}'.format(despesas_mes_atual.aggregate(total = Sum( 'valor_total'))['total']))
       
           

        except:
            despesas_mes_atual = 0
            quantidades_mes_atual = 0
            juros_mes_atual = 0
            despesas_mes_atual_valor_total = 0

        porcentagem_mes_atual = float('{0:.2f}'.format(porcentagem(despesas_mes_passado_valor_total, despesas_mes_atual_valor_total)))
        porcentagem_quantidades_mes_atual = porcentagem(quantidades_mes_passando, quantidades_mes_atual)
        portcetagem_unidade_mes_atual = porcentagem(total_unidades, quantidades_mes_atual)
        porcentagem_juros_mes_atual = porcentagem(juros_mes_passado, juros_mes_atual)
        porcentagem_porcentagem_mes_atual = porcentagem(porcentagem_mes_passado, porcentagem_mes_atual)
        


        return render(request, 'financeiro/contabilidade/contas/despesas.html', { 
            
            'despesas_mes_atual':despesas_mes_atual,'quantidades_mes_atual':quantidades_mes_atual,'juros_mes_atual':juros_mes_atual,
            'despesas_mes_atual_valor_total':despesas_mes_atual_valor_total,'porcentagem_mes_atual': porcentagem_mes_atual,
            'porcentagem_quantidades_mes_atual':porcentagem_quantidades_mes_atual,'porcentagem_juros_mes_atual':porcentagem_juros_mes_atual,
            'porcentagem_porcentagem_mes_atual':porcentagem_porcentagem_mes_atual,'data_atual':data_atual,
            'portcetagem_unidade_mes_atual':portcetagem_unidade_mes_atual,

            
            
            
            })






class Despesas_Manager_Details(LoginRequiredMixin, View):

    def get(self, request, despesas_id):
        despesa = get_object_or_404(Despesas, id = despesas_id)
        contas =  Conta.objects.all()
        condominios  = Condominios.objects.all()
        return render(request, 'financeiro/contabilidade/contas/details.html', {'despesa':despesa, 'contas':contas, 'condominios':condominios, })



class Pagamentos(LoginRequiredMixin, View):

    def post(self, request, despesas_id):
        
        despesa =get_object_or_404( Despesas, id = despesas_id)
        
        
        conta = request.POST.get("conta")           
        contas = Conta.objects.filter(id = conta)
        conta = get_object_or_404(Conta, id  = conta)
        conta.debitos += despesa.valor_total
        conta.save()
        contas.update(

                
                saldo = contas.aggregate(total=Sum(F('creditos') - F('debitos')))['total'],
            )

            
                 
        Movimentacao.objects.filter(conta = conta).get_or_create(

                    sindico_id = despesa.sindico_id,
                    conta = conta,
                    data = date.today(),
                    descricao = despesa.descricao,
                    tipo = 'D',
                    valor = despesa.valor_total,
                    saldo = conta.saldo - despesa.valor_total,
                ) 
        
        despesa.status = 'paga'
        despesa.save()

        return HttpResponseRedirect(reverse('financeiro:despesas_manager'))
        
#--------------------------------------- / END DESPESAS -------------------------------------------------


#--------------------------------------- RECEITAS MANAGEMENT -------------------------------------------------

class Receitas_View(View):

    def get(self, request):
        month_atual = '0{}/{}'.format(today.month, today.year)
        month = today.month

        total_unidades = Morador.objects.all().count()


        #-----------------------------2 Meses Anterior --------------------------------------------------------------------------------------------
        try:
            receita_mes_passado = Pagamento.objects.filter(data_vencimento__month = month - 2).order_by('unidade') 
            quantidade_mes_passado = Pagamento.objects.filter(data_vencimento__month = month - 2).count()
        except:
            receita_mes_passado = 0
            quantidade_mes_passado = 0
            

        #-----------------------------1 Meses Anterior --------------------------------------------------------------------------------------------
        try:
            receita_mes_anterior = Pagamento.objects.filter(data_vencimento__month = month - 1) 
            quantidade_mes_anterior = Pagamento.objects.filter(data_vencimento__month = month - 1).count()
        except:
            receita_mes_anterior = 0
            quantidade_mes_anterior = 0
       
        porcetagem_de_quantidade_anterior = porcentagem(quantidade_mes_anterior, quantidade_mes_passado)

        try:
            valor_total_pagamento_mes_anterior = float("{0:.2f}".format(receita_mes_anterior.aggregate(total = Sum('total'))['total']))
            juros_mes_anterior = float("{0:.2f}".format(receita_mes_anterior.aggregate(total = Sum('juros'))['total']))
        except:
            valor_total_pagamento_mes_anterior = float(0)
            juros_mes_anterior  = float(0)

        
        #-----------------------------Mês Atual  --------------------------------------------------------------------------------------------
        try:
            receitas_mes_atual = Pagamento.objects.filter(data_vencimento__month = month).order_by('unidade')
            
            quantidade_mes_atual = Pagamento.objects.filter(data_vencimento__month = month ).count()
        except:
            receitas_mes_atual = 0
            quantidade_mes_atual = 0        
        
        porcetagem_de_quantidade_mes_atual = porcentagem(quantidade_mes_anterior, quantidade_mes_atual)
        porcetagem_de_quantidade_comparacao = porcentagem(porcetagem_de_quantidade_mes_atual, porcetagem_de_quantidade_anterior)

        try:
            valor_total_pagamento_mes_atual = float("{0:.2f}".format(receitas_mes_atual.aggregate(total = Sum('valor_total'))['total']))
            juros_mes_atual = float("{0:.2f}".format(receitas_mes_atual.aggregate(total = Sum('multa'))['total']))
        except:
           # valor_total_pagamento_mes_atual = float(0)
            juros_mes_atual  = float(0)

        porcetagem_valor_total = float("{0:.2f}".format(porcentagem(valor_total_pagamento_mes_anterior, valor_total_pagamento_mes_atual)))
        porcetagem_valor_juros = float("{0:.2f}".format(porcentagem(juros_mes_anterior, juros_mes_atual)))  

        porcetagem_de_unidades_mes_atual  = porcentagem(total_unidades, quantidade_mes_atual)     
        return render(request, 'financeiro/contabilidade/receitas.html',{
            
            'month_atual':month_atual,'receitas_mes_atual':receitas_mes_atual ,'quantidade_mes_atual':quantidade_mes_atual, 'porcetagem_de_quantidade_mes_atual': porcetagem_de_quantidade_mes_atual,
            'porcetagem_de_quantidade_comparacao':porcetagem_de_quantidade_comparacao, 'valor_total_pagamento_mes_atual':valor_total_pagamento_mes_atual,
            'porcetagem_valor_total':porcetagem_valor_total, 'juros_mes_atual':juros_mes_atual, 'porcetagem_valor_juros':porcetagem_valor_juros,
            'porcetagem_de_unidades_mes_atual':porcetagem_de_unidades_mes_atual ,       
            })
            




#--------------------------------------- / END RECEITAS MANAGEMENT -------------------------------------------------
