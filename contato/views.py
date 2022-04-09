from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib import messages
from .forms import ContatoForm, NewletterForm



# Create your views here.







class Contato_View(View):

    def get(self, request):       
        if request.method == 'Get':
            form =ContatoForm(request.GET or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('index'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = ContatoForm()
        return render(request, 'contato/formulario.html',{'form':form, })


    def post(self, request):
        if request.method == 'POST':
            form = ContatoForm(request.POST or None, request.FILES or None )
            if form.is_valid():
                form.save()
                messages.success(request, 'Todos os dados são valido e serão inseridos no banco de dados ')
                return HttpResponseRedirect(reverse('index'))

            else:
                messages.error(request,'Ops...., os dados digitados estão incorretos, verificar novamente')

        else:
            form = ContatoForm()
        return render(request, 'contato/formulario.html', {'form':form})
        





