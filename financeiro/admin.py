from django.contrib import admin
from .models import Banco, Conta, Despesas, Movimentacao, Saldo_Anterior
from .models import Prazo, Categoria, SubCategoria, Inadimplência, Pagamento
from import_export.admin import ImportExportModelAdmin
import csv
from django.http import HttpResponse


class ExportCsvMixin:
    
    def admin_action(modeladmin, request, queryset):
        ModelAdmin = Inadimplência

    
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
# Register your models here.


@admin.register(Categoria)
class BancoAdmin(ImportExportModelAdmin):
    list_display = ['title']


@admin.register(SubCategoria)
class BancoAdmin(ImportExportModelAdmin):
    list_display = ['title']
    search_fields = ['title']



@admin.register(Banco)
class BancoAdmin(ImportExportModelAdmin):
    list_display = ['nome']



@admin.register(Conta)
class ContaAdmin(ImportExportModelAdmin):
    list_display = ['agencia', 'tipo' ,'debitos','creditos','saldo']
    


@admin.register(Despesas)
class DespesasAdmin(ImportExportModelAdmin):
    list_display = ['beneficiario','status','vencimento','pagamento','valor']

@admin.register(Movimentacao)
class MovimentacaoAdmin(ImportExportModelAdmin):
    list_display = ['conta', 'data','tipo','valor']


@admin.register(Saldo_Anterior)
class SaldoAnteriorAdmin(ImportExportModelAdmin):
    list_display = ['conta',]


@admin.register(Prazo)
class PrazoAdmin(ImportExportModelAdmin):
    list_display = ['title', 'status']



@admin.register(Inadimplência)
class InadimplenciaAdmin(ImportExportModelAdmin):
    list_display = ['morador','unidade','status','vencimento','boleto','juros','multa','atualizacao','honorarios','valor_total']
    list_filter = ['morador','vencimento']
    search_fields = ['morador',]

    def admin_action(modeladmin, request, queryset):
        ModelAdmin = Inadimplência

    
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response


    export_as_csv.short_description = "Selecinar Exportação"




@admin.register(Pagamento)
class PagamentoAdmin(ImportExportModelAdmin):
    list_display = ['morador', 'unidade',  'data_vencimento', 'data_pagamento', 'valor_total']
    list_filter = ['morador', 'unidade',  'data_vencimento', ]
    search_fields = ['morador', 'unidade',  'data_vencimento', 'data_pagamento', 'valor_total']




