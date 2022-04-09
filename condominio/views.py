from .forms import CondominiosForm, Taxas_Ordinaria_Form, Taxas_ExtraOrdinaria_Form, Contratos_Form
from .core import calculo_de_data_ocorrencias, calculo_diferenca_de_data, calculo_diferenca_da_data_atual, porcentagem
from .models import Condominios, Taxa_Extraordinaria, Taxa_Ordinaria, Ocorrencias, Contratos, Categoria, SubCategoria
from django.views.generic import View, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Sum ,F
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum ,F
from accounts.models import Administradores
from financeiro.models import Conta
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
import administration






class Manager_Condominio(LoginRequiredMixin, View):


    def get(self, request):        
        condominio = Condominios.objects.all()
        taxa_ordinaria = Taxa_Ordinaria.objects.all()
        bancos = Conta.objects.all() 
        try:
            valor_taxa = float(taxa_ordinaria.aggregate(total = Sum(F('taxa') + F('extra') + F('fundo')))['total'])
            

        except:
            valor_taxa = float(0)
        try:
            valor_total = float(condominio.aggregate(total = Sum(F('valor_taxa')))['total'],       )
        except:
            valor_total = float(0)

        condominio.update( 
            
            valor_total = valor_total,
            valor_taxa = valor_taxa,
        
        )
        print(valor_taxa)
        return render(request,'condominio/manager/residencial.html', {'residenciais':condominio, 'bancos':bancos })





class Adicionar_condominio(LoginRequiredMixin, View):

    def get(self, request):
        condominios = Condominios.objects.all()
        administradores = Administradores.objects.all()
        if request.method == 'Get':
            form =CondominiosForm(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('condominio.manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = CondominiosForm()
        return render(request, 'condominio/manager/adicionar.html',{'form':form, 'condominios':condominios, 'administradores':administradores})


    def post(self, request):
        if request.method == 'POST':
            form = CondominiosForm(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('condominio:manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = CondominiosForm()
        return render(request, 'condominio/manager/adicionar.html', {'form':form})
        





class Adicionar_Ordinaria(LoginRequiredMixin, View):

    def get(self, request):
        condominios = Condominios.objects.all()
        administradores = Administradores.objects.all()
        if request.method == 'Get':
            form = Taxas_Ordinaria_Form(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('condominio.manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Taxas_Ordinaria_Form()
        return render(request, 'condominio/manager/taxas_ordinaria.html',{'form':form, 'condominios':condominios,'administradores':administradores})


    def post(self, request):
        condominios = Condominios.objects.all()
        if request.method == 'POST':
            form = Taxas_Ordinaria_Form(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('condominio:manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Taxas_Ordinaria_Form()
        return render(request, 'condominio/manager/adicionar.html', {'form':form, 'condominios':condominios})
        


class Adicionar_ExtraOrdinaria(LoginRequiredMixin, View):

    def get(self, request):
        condominios = Condominios.objects.all()
        administradores = Administradores.objects.all()
        if request.method == 'Get':
            form = Taxas_ExtraOrdinaria_Form(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('condominio.manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Taxas_ExtraOrdinaria_Form()
        return render(request, 'condominio/manager/taxas_extraordinaria.html',{'form':form, 'condominios':condominios, 'administradores':administradores})


    def post(self, request):
        condominios = Condominios.objects.all()
        administradores = Administradores.objects.all()
        if request.method == 'POST':
            form = Taxas_ExtraOrdinaria_Form(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('condominio:manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Taxas_ExtraOrdinaria_Form()
        return render(request, 'condominio/manager/taxas_extraordinaria.html', {'form':form, 'condominios':condominios, 'administradores':administradores})
        


class Advertencias_View(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'condominio/manager/advertencias.html')


class Multas_View(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'condominio/manager/multas.html')


class Recursos_View(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'condominio/manager/recursos.html')\


class Ocorrencias_View(LoginRequiredMixin, View):

    def get(self, request):
        ocorrencias = Ocorrencias.objects.all()
        data = calculo_de_data_ocorrencias(datetime, Ocorrencias)
        total = Ocorrencias.objects.all().count()
        analizando = ocorrencias.filter( status = 'analizando').count()
        concluido = ocorrencias.filter( status = 'concluido').count()
        porcentagens = porcentagem(7, total)      
        return render(request, 'condominio/manager/ocorrencias.html',{
            
            'ocorrencias':ocorrencias, 'data':data, 'total':total,
            'analizando':analizando , 'concluido':concluido, 'porcentagens':porcentagens ,    
        
        
        })



class Autorizacoes_View(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'condominio/manager/autorizacoes.html')
        

class Informacoes_View(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'condominio/manager/informativos.html')



class Analytics_View(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'condominio/manager/analytics.html')




#---------------------------------------------- Contratos -------------------------------------------------------



class Contratos_View(LoginRequiredMixin, View):

     def get(self, request):
        contratos = Contratos.objects.all()
        for contrato in contratos:
            contrato
        tempo = calculo_diferenca_de_data(datetime, Contratos)
        data_atual = calculo_diferenca_da_data_atual(datetime, Contratos)
        percorrido = int(porcentagem(tempo, data_atual))        
        
        return render(request, 'condominio/manager/contrato/manager.html', {'contratos':contratos,'data_atual':data_atual, 'percorrido':percorrido})



class Adicionar_Contratos(LoginRequiredMixin, View):
    
    
    def get(self, request):
        categorias = Categoria.objects.all()
        subcategorias = SubCategoria.objects.all()
        if request.method == 'Get':
            form = Contratos_Form(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('condominio.manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Contratos_Form()
        return render(request, 'condominio/manager/contrato/adicionar.html',{'form':form, 'subcategorias':subcategorias, 'categorias':categorias})


    def post(self, request):
        categorias = Categoria.objects.all()
        subcaterias = SubCategoria.objects.all()
        if request.method == 'POST':
            form = Contratos_Form(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('condominio:manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Contratos_Form()
        return render(request, 'condominio/manager/contrato/adicionar.html', {'form':form, 'subcaterias':subcaterias, 'categorias':categorias})
        

