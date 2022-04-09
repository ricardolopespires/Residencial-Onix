from django.contrib import admin
from .models import Capitulo, Regimento_Interno, Checklist, Item

# Register your models here.

@admin.register(Capitulo)
class TitleRegimentoInterno(admin.ModelAdmin):
    list_display = ['title',]

@admin.register(Regimento_Interno)
class RegimentoInterno(admin.ModelAdmin):
    list_display = ['status']


@admin.register( Checklist )
class RegimentoInterno(admin.ModelAdmin):
    list_display = ['titulo']
    list_filter = ["titulo"]
    search_fields = ["titulo"]
    prepopulated_fields = {"slug": ("titulo",)}


@admin.register( Item )
class RegimentoInterno(admin.ModelAdmin):
    list_display = ['titulo']
    list_filter = ["titulo"]
    search_fields = ["titulo"]
    prepopulated_fields = {"slug": ("titulo",)}