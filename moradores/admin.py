from import_export.admin import ImportExportModelAdmin
from .models import Morador, Pessoa, Veiculo, Animal

from django.contrib import admin
from django.contrib.admin import AdminSite




class MoradoresAdminSite(AdminSite):
    site_header = "Condomínio Residencial Ônix Admin"
    site_title = "Condomínio Residencial Ônix Admin Portal"
    index_title = "Bem Vindo ao Portal do Condomínio Residencial Ônix"

moradores_admin_site = MoradoresAdminSite(name='moradores_admin')


moradores_admin_site.register(Morador)

# Register your models here.




@admin.register(Morador)
class MoradorAdmin(ImportExportModelAdmin):

    list_display = ['unidade','nome']


@admin.register(Veiculo)
class MoradorAdmin(ImportExportModelAdmin):

    list_display = ['placa','modelo']