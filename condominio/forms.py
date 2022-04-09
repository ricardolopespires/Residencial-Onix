from django import forms
from django.forms import fields
from condominio.models import Condominios, Taxa_Ordinaria, Taxa_Extraordinaria, Contratos





class CondominiosForm(forms.ModelForm):


    class Meta:
        model = Condominios
        fields = ('__all__')


class Taxas_Ordinaria_Form(forms.ModelForm):
   
    class Meta:
        model = Taxa_Ordinaria
        fields = ('__all__')


class Taxas_ExtraOrdinaria_Form(forms.ModelForm):

    class Meta:
        model = Taxa_Extraordinaria
        fields = ('__all__')



class Contratos_Form(forms.ModelForm):


    class Meta:

        model = Contratos
        fields = ('__all__')

        