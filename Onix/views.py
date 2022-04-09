from django.views.generic import View, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import routers, serializers, viewsets
from django.http import HttpResponseRedirect
from condominio.models import Condominios
from contato.forms import NewletterForm
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
#from .serializers import CondominioSerializer




class IndexView(View):

    def get(self, request):
        return render(request,'initial/index.html')



class About_View(View):
    
    def get(self, request):
        return render(request,'initial/about.html')

class Servicos_View(LoginRequiredMixin,View):
    
    def get(self, request):
        return render(request,'initial/servicos.html')

class Projetos_View(LoginRequiredMixin, View):
    
    def get(self, request):
        return render(request,'initial/projetos.html')



class Newletter(View):

    def get(self, request):       
        if request.method == 'Get':
            form =NewletterForm(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('index'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = NewletterForm()
        return render(request, 'initial/index.html',{'form':form, })


    def post(self, request):
        if request.method == 'POST':
            form = NewletterForm(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('index'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = NewletterForm()
        return render(request, 'initial/index.html', {'form':form})
        


'''
# ViewSets define the view behavior.
class CondominioViewSet(viewsets.ModelViewSet):
    queryset = Condominios.objects.all()
    serializer_class = CondominioSerializer
'''

    


    