from django.views.generic import View, TemplateView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count, Sum ,F
from django.http import HttpResponseRedirect
from .models import Morador, Pessoa, Veiculo, Animal, Funcionario
from financeiro.models import Inadimplência
from django.contrib import messages
from .forms import MoradoresForm, Veiculo_Form, Animal_Form, Funcionario_Form
from django.urls import reverse

# Create your views here.



class Manager_Moradores_View(LoginRequiredMixin,View):

    def get(self, request):
        moradores = Morador.objects.all().order_by('id')        
        return render(request, 'moradores/manager.html',{'moradores':moradores})


class Moradores_DetailView(LoginRequiredMixin,View):

    def get(self, request, pk):
        moradores = get_object_or_404(Morador, unidade=pk) 
        veiculos = Veiculo.objects.filter(morador = moradores)
        inadinplencias = Inadimplência.objects.filter(morador = moradores)     
        return render(request, 'moradores/details.html',{
            
            'moradores':moradores, 'inadinplencias':inadinplencias,
            'veiculos':veiculos,
            
            
            })




class Adicionar_Morador(LoginRequiredMixin,View):

    def get(self, request):
        parentes = Pessoa.objects.all()
        if request.method == 'GET':
            form = MoradoresForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
        else:
            form = MoradoresForm()
        return render(request, 'moradores/adicionar.html',{'form':form, 'parentes':parentes})



    def post(self, request):
        parentes = Pessoa.objects.all()
        if request.method == 'POST':
            form = MoradoresForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Os Dados estão corretos e serão gravado no seu banco de dados')
                return HttpResponseRedirect(reverse('moradores:manager'))
            else:
                messages.error(request, 'Ops.... Os dados preenchido estão errados, Por favor Corrigi-los')
            
        else:
            form = MoradoresForm()
        return  render(request, 'moradores/adicionar.html',{'form':form,'parentes':parentes })



class Morador_Update_View(LoginRequiredMixin, UpdateView):
    model = Morador
    fields = ['id']

    success_url = 'moradores/manager/'


def morador_update(request, pk):
    moradores = get_object_or_404(Morador, id = pk)    
    form = MoradoresForm(request.POST or None, request.FILES or None, instance  = moradores)  
   
    if form.is_valid():
       
        form.save()        
        messages.success(request, 'Seu novo Cliente foi salvo com sucesso !!!!')
        return HttpResponseRedirect(reverse('moradores:manager'))

    return render(request, 'moradores/updated.html', {'form':form})


    
class Veiculos_View(View):
    def get(self, request):
        veiculos = Veiculo.objects.all()
        return render(request, 'moradores/veiculos/manager.html',{'veiculos':veiculos})



class Veiculos_Detail_View(View):
    def get(self, request, veiculo_id):
        veiculo = get_object_or_404(Veiculo, id = veiculo_id)
        return render(request, 'moradores/veiculos/details.html',{'veiculo':veiculo})



class Adicionar_Veiculo(LoginRequiredMixin,View):

    def get(self, request):
        moradores = Morador.objects.all()
        return render (request, 'moradores/veiculos/adicionar.html', {'moradores':moradores})


    def post(self, request):
        moradores = Morador.objects.all()
        if request.method == 'POST':
            form = Veiculo_Form(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Os dados do veiculo estão corretos e serão gravado no seu banco de dados')
                return HttpResponseRedirect(reverse('moradores:manager'))
            else:
                messages.error(request, 'Ops.... Os dados preenchido do veiculo estão errados, Por favor Corrigi-los')
            
        else:
            form = Veiculo_Form()
        return  render(request, 'moradores/veiculos/adicionar.html',{'form':form, 'moradores':moradores})


class Animal_View(View):
    def get(self,request):
        return render(request, 'moradores/animal/manager.html')



class Adicionar_Animais(LoginRequiredMixin,View):

    def get(self, request):
        moradores = Morador.objects.all()
        return render (request, 'moradores/animal/adicionar.html', {'moradores':moradores})


    def post(self, request):
        moradores = Morador.objects.all()
        if request.method == 'POST':
            form = Animal_Form(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Os dados do animal estão corretos e serão gravado no seu banco de dados')
                return HttpResponseRedirect(reverse('moradores:manager'))
            else:
                messages.error(request, 'Ops.... Os dados preenchido do animal estão errados, Por favor Corrigi-los')
            
        else:
            form = Animal_Form()
        return  render(request, 'moradores/animal/adicionar.html',{'form':form, 'moradores':moradores})


class Funcionario_View(View):
    def get(self, request):        
        return render(request, 'moradores/funcionarios/manager.html',)



class Adicionar_funcionario(LoginRequiredMixin,View):

    def get(self, request):
        moradores = Morador.objects.all()
        return render (request, 'moradores/funcionarios/adicionar.html', {'moradores':moradores})


    def post(self, request):
        moradores = Morador.objects.all()
        if request.method == 'POST':
            form = Funcionario_Form(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Os dados do animal estão corretos e serão gravado no seu banco de dados')
                return HttpResponseRedirect(reverse('moradores:manager'))
            else:
                messages.error(request, 'Ops.... Os dados preenchido do animal estão errados, Por favor Corrigi-los')
            
        else:
            form = Funcionario_Form()
        return  render(request, 'moradores/funcionarios/adicionar.html',{'form':form, 'moradores':moradores})




class Analytics_Moradores(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'moradores/analytics.html')