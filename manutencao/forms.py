from django import forms
from django.forms import fields
from django.forms.models import ModelForm
from .models import Item, Manutencao








class Item_Form(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('__all__')



class Manutencao_Form(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ('__all__')


