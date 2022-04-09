from django import forms
from django.db.models import fields
from .models import Funcionario, Salario





class Funcionario_Form(forms.ModelForm):

    class Meta:
        model  = Funcionario
        fields = ('__all__')




class Salario_Form(forms.ModelForm):

    class Meta:
        model = Salario
        fields = ('__all__')



