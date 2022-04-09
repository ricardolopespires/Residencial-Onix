from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Funcionario, Salario, Avaliacao
# Register your models here.





@admin.register(Funcionario)
class FuncionarioAdmin(ImportExportModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']
    search_fields = ['nome'] 



@admin.register(Salario)
class FuncionarioAdmin(ImportExportModelAdmin):
    list_display = ['funcionario','mes_referente','salario_bruto','vale_transporte','vale_refeicao','salario_liquido']
    list_filter = ['funcionario']
    search_fields = ['funcionario'] 



@admin.register(Avaliacao)
class AvaliacaoAdmin(ImportExportModelAdmin):
    list_display = ['user', 'funcionario','date', 'rate']

