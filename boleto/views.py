# Create your views here.
from django.views.generic import View, TemplateView, DetailView
from financeiro.models import Pagamento, Conta, Movimentacao
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from dateutil.relativedelta import relativedelta
from django.db.models import Avg, Count, Sum ,F
from pyboleto.pdf import BoletoPDF, load_image
from django.http import HttpResponseRedirect 
from condominio.models import Condominios
from .core import calculo_entre_datas
from django.http import HttpResponse
from moradores.models import Morador
from django.contrib import messages
from django.contrib import admin
from django.urls import reverse
from datetime import datetime
from decimal import Decimal
from .models import Boleto
from datetime import date
import numpy as np
import random
import boleto


class Boleto_View(LoginRequiredMixin, View):

    def get(self,request):
        boletos = Boleto.objects.filter( status = 'aberto').order_by('unidade')
        data_restante = calculo_entre_datas(boletos, datetime, date, relativedelta)            
        return render(request, 'boleto/manager.html', {'boletos':boletos,'data_restante':data_restante})


class Boleto_Pagamento(LoginRequiredMixin, View):

    def get(self, request, pk):
        data_atual = date.today()
        boleto = get_object_or_404(Boleto, unidade = pk)
        sacado =get_object_or_404(Morador, unidade = boleto.unidade)
        cedentes = Condominios.objects.all()
        contas = Conta.objects.all()
        return  render (request, 'boleto/pagamento.html', {
            
            'boleto':boleto, 'sacado':sacado, 'cedentes':cedentes,
            'data_atual':data_atual,'contas':contas,
            
            })


class Pagamento_View(LoginRequiredMixin, View):


    def get(self, request, pk):
        boleto = get_object_or_404(Boleto, unidade = pk)
        sacado =get_object_or_404(Morador, unidade = boleto.unidade)
        return HttpResponseRedirect(reverse('boletos:manager'))



    def post(self, request, pk):
        boleto = get_object_or_404(Boleto, unidade = pk)
        sacado =get_object_or_404(Morador, unidade = boleto.unidade)
        
        cedentes = Condominios.objects.all()
        for cedente in cedentes:
            cedente        

        # Criar o array 3 x 3 com números aleatórios entre 1 e 52
        numero_ordem = random.randint(0,10000)     


        if request.method == 'POST':           
            data_do_pagamento = request.POST.get('data_do_pagamento') 
                    

            Pagamento.objects.create(

            id = numero_ordem,
            unidade = boleto.unidade,
            morador_id = sacado.id,
            data_vencimento = boleto.data_vencimento,
            data_pagamento = data_do_pagamento,
            valor_total = boleto.valor_documento,
        )

        conta = get_object_or_404(Conta, tipo = 'conta corrente')
        

        valor_documento =  Decimal(boleto.valor_documento - Decimal(3.93))
        valor_total  = conta.saldo + valor_documento      

        conta.creditos += valor_documento
        conta.saldo += valor_documento
        conta.save()

        Movimentacao.objects.filter(conta = conta).get_or_create(

                    sindico_id = conta.sindico_id,
                    conta = conta,
                    data = date.today(),
                    descricao = 'unidade pagante: ' + str( boleto.unidade),
                    tipo = 'C',
                    valor = valor_documento,
                    saldo = valor_total,
                ) 

        print(float(valor_documento))
        boleto.status = 'pago'
        boleto.save()
        cedente.receitas +=  valor_documento 
        cedente.save()
        sacado.taxa = 0
        sacado.save()
        valor_total = Morador.objects.filter( unidade = boleto.unidade).aggregate(total = Sum(F('taxa') + F('taxa_extra')))['total']
        
        Morador.objects.filter( unidade = boleto.unidade).update(valor_total = valor_total,)
        
        return HttpResponseRedirect(reverse('boletos:manager'))


        



class Print_boleto(LoginRequiredMixin, View):

    def get(modeladmin, request, queryset, numero_documento):
        from io import StringIO
        buffer = StringIO()
        boleto_pdf = BoletoPDF(buffer)

        for b in queryset:       
            b.print_pdf_pagina(boleto_pdf)
            boleto_pdf.nextPage()
        boleto_pdf.save()

        pdf_file = buffer.getvalue()

        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=%s' % (
            u'boletos_%s.pdf' % (
                date.today().strftime('%Y%m%d'),
            ),
        )
        response.write(pdf_file)
        return response