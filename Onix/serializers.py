from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import  serializers
from condominio.models import Condominios

# Serializers define the API representation.
class CondominioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condominios
        fields = ('__all__')