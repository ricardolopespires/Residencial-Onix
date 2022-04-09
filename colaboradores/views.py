from django.views.generic import View, TemplateView, DetailView
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg, Count, Sum ,F, Q
from django.http import HttpResponseRedirect
from condominio. models import Condominios
from accounts.models import Administradores
from .forms import Funcionario_Form
from django.contrib import messages
from django.urls import reverse
from .models import Funcionario, Salario, Avaliacao
from .core import porcentagem
# Create your views here.




class Funcionarios_Manager(View):

    def get(self, request):
        funcionarios = Funcionario.objects.all()
        administradores = Administradores.objects.all()

        return render(request, 'funcionarios/manager.html', {'funcionarios':funcionarios,})




class Adicionar_funcionario(View):

    def get(self, request):
        condominios = Condominios.objects.all()
        administradores = Administradores.objects.all()
        if request.method == 'Get':
            form = Funcionario_Form(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('colaboradores:manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Funcionario_Form()
        return render(request, 'funcionarios/manager/adicionar.html',{'form':form, 'condominios':condominios,'administradores':administradores,})


    def post(self, request):
        condominios = Condominios.objects.all()
        administradores = Administradores.objects.all()
        if request.method == 'POST':
            form = Funcionario_Form(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('colaboradores:manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Funcionario_Form()
        return render(request, 'funcionarios/manager/adicionar.html', {'form':form, 'condominios':condominios,'administradores':administradores,})
        



class Funcionarios_Details(View):

    def get(self, request, pk):
        funcionario = get_object_or_404(Funcionario, id = pk)
        salarios = Salario.objects.filter(funcionario = funcionario)
        avaliacao = Avaliacao.objects.filter(funcionario = funcionario)
        avaliacao_total = Avaliacao.objects.filter(funcionario = funcionario).count()
        try:
            excelente_total =  avaliacao.filter(rate__startswith = 5).count()
        except:
            excelente_total = 0

        try:
            bom_total = avaliacao.filter(rate__startswith = 4 ).count()
        except:
            bom_total = 0

        try:
            media_total = avaliacao.filter(rate__startswith = 3 ).count()
        except:
            media_total = 0

        try:
            ruim_total = avaliacao.filter(rate__startswith = 2 ).count()
        except:
            ruim_total = 0

        try:
            pessimo_total = avaliacao.filter(rate__startswith = 1 ).count()
        except:
            pessimo_total = 0
        
        try:
            media_avaliacao = avaliacao.aggregate(Avg('rate'))['rate__avg']
        except:
            media_avaliacao = 0

        
        porcentagem_exelente = int(porcentagem(avaliacao_total, excelente_total))
        porcentagem_bom = int(porcentagem(avaliacao_total, bom_total))
        porcentagem_media = int(porcentagem(avaliacao_total, media_total))
        porcentagem_ruim = int(porcentagem(avaliacao_total, ruim_total))
        porcentagem_pessimo = int(porcentagem(avaliacao_total, pessimo_total))
                
        
        print(media_avaliacao)
        salarios.update(salario_liquido= Salario.objects.aggregate(total=Sum(F('salario_bruto') + F('vale_transporte') + F('vale_refeicao')))['total'])
        return render(request, 'funcionarios/manager/details.html', {
            
            'funcionario':funcionario, 'salarios':salarios, 'avaliacao':avaliacao,'media_avaliacao':media_avaliacao,
            'excelente_total':excelente_total ,'bom_total':bom_total,'media_total':media_total, 'ruim_total':ruim_total,
            'pessimo_total':pessimo_total,'porcentagem_exelente': porcentagem_exelente,'porcentagem_bom':porcentagem_bom,
            'porcentagem_media':porcentagem_media,'porcentagem_ruim':porcentagem_ruim,'porcentagem_pessimo':porcentagem_pessimo, 
            
            })



class Avalicao_details(View):


    def get(self, request, pk):
        funcionario = get_object_or_404(Funcionario, id = pk)
        return render(request, 'funcionarios/manager/avaliacao_details.html', {'funcionario':funcionario,})