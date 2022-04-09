from import_export.admin import ImportExportModelAdmin
from .models import Item, Manutencao
from django.contrib import admin

# Register your models here.





@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):

    list_display = ['local','nome']



@admin.register(Manutencao)
class ItemAdmin(ImportExportModelAdmin):

    list_display = ['status','tipo', 'item']