from django import forms
from .models import Morador, Veiculo, Animal, Funcionario



class MoradoresForm(forms.ModelForm):

    class Meta:
        model = Morador
        fields = ('__all__')



class Veiculo_Form(forms.ModelForm):

    class Meta:
        model = Veiculo
        fields = ('__all__')


class Animal_Form(forms.ModelForm):

    class Meta:
        model = Animal
        fields = ('__all__')



class Funcionario_Form(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ('__all__')



        