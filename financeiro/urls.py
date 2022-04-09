from financeiro.models import Acordo
from boleto.views import Pagamento_View
from django.urls import path
from . import views



app_name = 'financeiro'



urlpatterns = [ 


    #--------------------------------- CONTABILIDADE ----------------------------------------------------------------------


    path('contabilidade/manager/',views.Contabilidade_Manager.as_view(), name = 'contabilidade'),


    #--------------------------------- INADINPLÊNCIA ------------------------------------------------------------------------

    path('inadinplencias/mes/anterior', views.Inadimplencia_Mes_Anterior_View.as_view(), name = 'inadinplencias_mes_anterior'),   
    path('inadinplencias/mes/atual', views.Inadimplencia_Mes_Atual_View.as_view(), name = 'inadinplencias_mes_atual'),
    path('inadinplencias/ano/passado/', views.Inadimplencia_Ano_Passado_View.as_view(), name = 'inadinplencias_ano_passado'),
    path('inadinplencias/ano/atual/', views.Inadimplencia_Anual_View.as_view(), name = 'inadinplencias_anual'),
    path('boleto/<pk>/pagamento/', views.Boleto_Pagamento.as_view(), name = 'boleto_pagamento'),
    path('pagamento/<pk>/inadimplencias/',views.Pagamento_View.as_view(), name = 'inadimplencia_pagamentos'),    




    path('receitas/',views.Receitas_View.as_view(), name = 'receitas'),   
    path('multas',views.Multas_View.as_view(), name = 'multas'),   
    path('juridicos/',views.Juridico_View.as_view(), name = 'juridicos'),


    #--------------------------------- ACORDOS --------------------------------------------------------------------------------------------------

    path('acordos/manager',views.Acordos_View.as_view(), name = 'acordo_manager'),
    path('acordos/created/',views.Created_Acordo.as_view(), name = 'created_acordo'),
    path('acordo/',views.Acordo.as_view(), name = 'acordo'),

    

    #--------------------------------- BANCOS -----------------------------------------------------------------------------------------------------

    path('bancos/', views.Banco_Manager.as_view(), name = 'bancos'),
    path('adicionar/banco/', views.Adicionar_Banco.as_view(), name = 'adicionar_banco'),
    path('bancos/<pk>/contas/', views.Conta_Manager.as_view(), name = 'contas'),
    path('bancos/deposito/<conta_id>/conta/',views.Deposito_View.as_view(), name = 'deposito'),
    path('banco/contas/<pk>/extrato/', views.Extrato_Conta.as_view(), name = 'extrato_conta'),
    path('banco/adicionar/conta/', views.Adicionar_Contas.as_view(), name = 'adicionar_contas'),



    #--------------------------------- DESPESAS --------------------------------------------------------------------------
    path('despesas/manager/',views.Despesas_Manager.as_view(), name = 'despesas_manager'),
    path('despesas/<despesas_id>/details/', views.Despesas_Manager_Details.as_view(), name = 'despesas_details'),
    path('despesa/', views.Adicionar_Despesas_Mensal.as_view(), name = 'adicionar_despesas'),
    path('pagamentos/<despesas_id>/details/',views.Pagamentos.as_view(), name = 'pagamentos'),

    #---------------------------------- Receitas --------------------------------------------------------------------------
    path('receitas/',views.Receitas_View.as_view(), name = 'receitas'),\

]



