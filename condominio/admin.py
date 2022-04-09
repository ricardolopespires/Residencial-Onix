from django.contrib import admin
from .models  import Condominios, Taxa_Ordinaria, Taxa_Extraordinaria, Advertencia, Multa, Ocorrencias, Categoria, SubCategoria, Contratos
from .models import Recurso_Multa 
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(Condominios)
class CondominiosAdmin(ImportExportModelAdmin):
    list_display = ['nome', 'receitas','despesas', 'caixa']



@admin.register(Taxa_Ordinaria)
class CondominiosAdmin(ImportExportModelAdmin):
    list_display = ['taxa']



@admin.register(Taxa_Extraordinaria)
class CondominiosAdmin(ImportExportModelAdmin):
    list_display = ['valor']



@admin.register(Advertencia)
class CondominiosAdmin(ImportExportModelAdmin):
    list_display = ['morador']


@admin.register(Ocorrencias)
class CondominiosAdmin(ImportExportModelAdmin):
    list_display = ['declarante','unidade', 'declarado','unidade_envolvida']



@admin.register(Categoria)
class CondominiosAdmin(ImportExportModelAdmin):
    list_display = ['title']



@admin.register(SubCategoria)
class CondominiosAdmin(ImportExportModelAdmin):
    list_display = ['title','categorie']



@admin.register(Contratos)
class CondominiosAdmin(ImportExportModelAdmin):
    list_display = ['empresa']



