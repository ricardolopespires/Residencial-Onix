from django.urls.base import is_valid_path
from .forms import Regimento_Interno_Form, Capitulo_Form, Checklist_Form, Item_Form 
from .models import Capitulo, Regimento_Interno, Checklist, Item
from django.views.generic import View, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from accounts.models import User, Administradores
from dateutil.relativedelta import relativedelta
from accounts.forms import Administadores_Form
from django.http import HttpResponseRedirect
from .core import calculo_entre_datas, procetagem_diaria
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
import administration

from moradores.models import Morador

# Create your views here.


class Administarion_View_Mandato(LoginRequiredMixin, View):

    def get(self, request):
        administradores = Administradores.objects.all()
        for administrador in administradores:
           tempo = calculo_entre_datas(administrador.data_de_inicio, administrador.termino,  datetime, relativedelta )
           porcentagem = int(procetagem_diaria(tempo['tempo_total'], tempo['tempo_parcial'] ))
                     
           print(porcentagem)
        return render(request, 'administration/mandato/list.html', {'administradores':administradores ,'tempo':tempo, 'porcentagem':porcentagem})



class Administarion_Details(LoginRequiredMixin, View):

    def get(self, request, pk):
        administrador = get_object_or_404(Administradores,id = pk)
        return render(request, 'administration/mandato/details.html', {'administrador':administrador})



class Adicionar_administradores(LoginRequiredMixin,View):

    def get(self, request):        
        usuarios = User.objects.all()
        if request.method == 'Get':
            form = Administadores_Form(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('administration:mandato'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Administadores_Form()
        return render(request, 'administration/mandato/adicionar.html',{'form':form, 'usuarios':usuarios})


    def post(self, request):
        usuarios = User.objects.all()
        if request.method == 'POST':
            form = Administadores_Form(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('administration:mandato'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Administadores_Form()
        return render(request, 'administration/mandato/adicionar.html', {'form':form, 'usuarios':usuarios})
        


class Administarion_View_Documentos(LoginRequiredMixin, View):

    def get(self, request):
        administradores = Administradores.objects.all()
        return render(request, 'administration/documentos/manager.html', )


class Administarion_View_Regimento_Interno(LoginRequiredMixin, View):

    def get(self, request):
        capitulos= Capitulo.objects.all()        
        return render(request, 'administration/documentos/regimento_interno/manager.html',{'capitulos':capitulos})




class Adicionar_Capitulos_Regimento_Interno(LoginRequiredMixin,View):

    def get(self, request):        
        capitulos = Capitulo.objects.all()
        if request.method == 'Get':
            form = Capitulo_Form(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('administration:regimento_interno'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Capitulo_Form()
        return render(request, 'administration/documentos/regimento_interno/adicionar_capitulos.html',{'form':form, 'capitulos':capitulos})


    def post(self, request):
        capitulos = Capitulo.objects.all()
        if request.method == 'POST':
            form = Capitulo_Form(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('administration:regimento_interno'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Capitulo_Form()
        return render(request, 'administration/documentos/regimento_interno/adicionar_capitulos.html', {'form':form, 'cpitulos':capitulos})
        




class Administarion_View_Regimento_Interno_Codigos(LoginRequiredMixin, View):

    def get(self, request, title_id):            
        normas  = Regimento_Interno.objects.filter(title = title_id)
        
        return render(request, 'administration/documentos/regimento_interno/normas.html',{ 'normas':normas})




class Adicionar_Normas_Regimento_Interno(LoginRequiredMixin,View):

    def get(self, request):        
        capitulos = Capitulo.objects.all()
        if request.method == 'Get':
            form = Regimento_Interno_Form(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('administration:regimento_interno'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Regimento_Interno_Form()
        return render(request, 'administration/documentos/regimento_interno/adicionar.html',{'form':form, 'capitulos':capitulos})


    def post(self, request):
        capitulos = Capitulo.objects.all()
        if request.method == 'POST':
            form = Regimento_Interno_Form(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('administration:regimento_interno'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Regimento_Interno_Form()
        return render(request, 'administration/documentos/regimento_interno/adicionar.html', {'form':form, 'cpitulos':capitulos})
        


class Administarion_View_Checklist(LoginRequiredMixin, View):

    def get(self, request):
        checklists = Checklist.objects.all()   
        return render(request, 'administration/checklist/manager.html',{'checklists':checklists} )


class Administarion_View_Checklist_Details(LoginRequiredMixin, View):

    def get(self, request, slug): 
        checklist = get_object_or_404(Checklist, slug = slug)       
        items = Item.objects.filter(documentos = checklist)      
        return render(request, 'administration/checklist/item/checklist.html',{'checklist':checklist, 'items':items} )




class Adicionar_Checklist_Item(LoginRequiredMixin,View):

    def get(self, request):        
        capitulos = Capitulo.objects.all()
        if request.method == 'Get':
            form = Item_Form(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('administration:checklist'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Item_Form()
        return render(request, 'administration/checklist/item/adicionar.html',{'form':form, 'capitulos':capitulos})


    def post(self, request):
        capitulos = Capitulo.objects.all()
        if request.method == 'POST':            
            titulo = request.POST.get("titulo").capitalize()
            slug = request.POST.get("slug")
            descricao = request.POST.get("descricao").capitalize()
            data_entrega =  request.POST.get("data_entrega")
            documentos = request.POST.get('documentos')
            documentos = Checklist.objects.get(id = documentos)
            status = request.POST.get("status")
            complete_per = request.POST.get('complete_per')

            item = Item(

                titulo = titulo,
                status = status,
                slug = slug,
                descricao = descricao,
                data_entrega = data_entrega,
                documentos = documentos,
                complete_per = complete_per,
                
               
            )
            item.save()            
            messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
            return HttpResponseRedirect(reverse('administration:checklist'))           

        
        return render(request, 'administration/checklist/item/adicionar.html', {'capitulos':capitulos})
        



class Administarion_View_Votacao(LoginRequiredMixin, View):

    def get(self, request):
        administradores = Administradores.objects.all()
        return render(request, 'administration/votacao/manager.html', )





class Autorizacoes_Moradores_view(LoginRequiredMixin, View):

    def get(self, request):
        usuarios = User.objects.all()
        is_authenticated = get_object_or_404(Morador, unidade =  request.user.unidade )        
      
        return render(request, 'administration/autorizacao/manager.html', {'usuarios':usuarios, 'is_authenticated':is_authenticated, } )
