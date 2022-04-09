from django import forms
from django.forms import fields
from .models import Regimento_Interno, Capitulo, Checklist, Item



class Regimento_Interno_Form(forms.ModelForm):

    class Meta:
        model = Regimento_Interno
        fields = ('__all__')


class Capitulo_Form(forms.ModelForm):

    class Meta:
        model = Capitulo
        fields = ('__all__')


class Checklist_Form(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ('__all__')



class Item_Form(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('__all__')