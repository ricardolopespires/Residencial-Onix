from django.views.generic import View, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from dateutil.relativedelta import relativedelta
from django.db.models import Avg, Count, Sum ,F
from .forms import Item_Form, Manutencao_Form
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from .models import Item, Manutencao
from django.urls import reverse
from datetime import date

today = date.today()



class  Mantuncao_Manager(LoginRequiredMixin, View):

    def get(self, request):
        data_atual = '0{}/{}'.format(today.month, today.year)
        month = today.month
        manutencoes = Manutencao.objects.all()

        total = Manutencao.objects.all().count()

        preventiva = Manutencao.objects.filter(tipo = 'preventiva').count()
        preditiva = Manutencao.objects.filter(tipo = 'preditiva').count()
        corretiva = Manutencao.objects.filter(tipo = 'corretiva').count()

        try:
            valor_total = Manutencao.objects.filter(status__startswith = "realizada").aggregate(total = Sum('valor_total'))['total']
        except:
            valor_total = 0


        return render(request,'manutencao/manager.html',{
            
            'data_atual':data_atual, 'manutencoes':manutencoes,'total':total,'preventiva':preventiva,
            'preditiva':preditiva,'corretiva':corretiva,'valor_total':valor_total,
            
            })



class Manutencao_Item_View(LoginRequiredMixin, View):

    def get(self, request, manutencao_id):
        data_atual = '0{}/{}'.format(today.month, today.year)
        month = today.month
        manutencao = get_object_or_404(Manutencao, id = manutencao_id)
        return render(request, 'manutencao/item.html',{'data_atual':data_atual, 'manutencao':manutencao})





class Agendamento(LoginRequiredMixin, View):

    def get(self, request):        
        itens = Item.objects.all()
        if request.method == 'Get':
            form = Manutencao_Form(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('manutencao.manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Manutencao_Form()

        return render(request, 'manutencao/agendamento.html',{'form':form, 'itens':itens})


    def post(self, request):
        
        itens = Item.objects.all()
        if request.method == 'POST':
            form = Manutencao_Form(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('manutencao:manager'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = Manutencao_Form()
        return render(request, 'condominio/manager/adicionar.html', {'form':form , 'itens':itens})
        
