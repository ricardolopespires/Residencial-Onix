from django import forms
from django.db import models
from django.db.models import fields
from .models import Banco, Conta, Movimentacao, Despesas






class BancoForm(forms.ModelForm):

    class Meta:
        model = Banco
        fields = ('__all__')



class ContasForm(forms.ModelForm):
    
    class Meta:
        model = Conta
        fields = ('__all__')



class Deposito_Form(forms.Form):
  
    valor = forms.DecimalField(decimal_places = 2, max_digits = 10, help_text="Valor do depósito")


class Despesas_Mensal_Form(forms.ModelForm):


    class Meta:
        model = Despesas
        fields = ('__all__')



class Movimentacao_Form(forms.ModelForm):


    class Meta:
        model = Movimentacao
        fields = ('__all__')