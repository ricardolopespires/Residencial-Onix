from django import forms
from django.db.models import fields
from .models import Contato, Newletter






class ContatoForm(forms.ModelForm):

    class Meta:

        model = Contato
        fields = ('__all__')




class NewletterForm(forms.ModelForm):

    class Meta:

        model = Newletter
        fields = ('__all__')