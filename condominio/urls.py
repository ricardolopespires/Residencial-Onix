from django.urls import path
from . import views




app_name = 'condominio'



urlpatterns = [

    path('manager/', views.Manager_Condominio.as_view(), name = 'manager'),
    path('adicionar/condominio/', views.Adicionar_condominio.as_view(), name = 'adicionar'),
    path('adicionar/taxas/ordinaria', views.Adicionar_Ordinaria.as_view(), name = 'taxas_ordinaria' ),
    path('adicionar/taxas/extraordinaria', views.Adicionar_ExtraOrdinaria.as_view(), name = 'taxas_extraordinaria' ),

    #--------------------------------------- Contratos ----------------------------------------------------------------
    path('contrato/',views.Contratos_View.as_view(), name = 'contratos'),
    path('contrato/adicionar/', views.Adicionar_Contratos.as_view(), name = 'adicionar_contratos'),


    path('advertencias/',views.Advertencias_View.as_view(), name = 'advertencias'),
    path('multas/',views.Multas_View.as_view(), name = "multas"),
    path('recursos/',views.Recursos_View.as_view(), name = 'recurso'),
    path('ocorrencias/',views.Ocorrencias_View.as_view(), name = 'ocorrencias'),
    path('autorizacoes/', views.Autorizacoes_View.as_view(), name = 'autorizacoes'),
    path('informativos/',views.Informacoes_View.as_view(), name = 'informativos'),
    path('analytics/',views.Analytics_View.as_view(), name = 'analytics'),

]



