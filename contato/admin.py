from django.contrib import admin
from .models import Contato, Newletter

# Register your models here.


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ['nome']


@admin.register(Newletter)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ['email']