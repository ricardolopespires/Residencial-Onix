from django.urls import path
from . import views




app_name = 'administration'




urlpatterns = [ 

    path('mandato/', views.Administarion_View_Mandato.as_view(), name = 'mandato'),
    path('adicionar/membros/',views.Adicionar_administradores.as_view(), name = 'adicionar_membros'),
    path('adminstadore/<pk>/details',views.Administarion_Details.as_view(), name = 'administrador_details'),
    path('documentos/',views.Administarion_View_Documentos.as_view(), name = 'documentos'),
    path('documentos/regimento/interno/',views.Administarion_View_Regimento_Interno.as_view(), name = 'regimento_interno'),
    path('documentos/regimento/interno/<title_id>/codigo/',views.Administarion_View_Regimento_Interno_Codigos.as_view(), name = 'codigos'),
    path('adicionar/capitulos/regimento/interno/',views.Adicionar_Capitulos_Regimento_Interno.as_view(), name = 'adicionar_capitulos'),
    path('adicionar/normas/regimento/interno/',views.Adicionar_Normas_Regimento_Interno.as_view(), name = 'adicionar_normas'),
    path('autorizacoes/moradores/',views.Autorizacoes_Moradores_view.as_view(), name = 'autorizacao_moradores'),

    #---------------------------------------------- Checklist --------------------------------------------------------------------------------
    path('trasincao/checklist/documentos/',views.Administarion_View_Checklist.as_view(), name = 'checklist'),
    path('trasincao/checklist/documentos/<slug>/deatils/',views.Administarion_View_Checklist_Details.as_view(), name = 'checklist_details'),
    path('trasincao/checklist/adicionar/item/', views.Adicionar_Checklist_Item.as_view(), name = 'adicionar_itens'),


     #---------------------------------------------- Votação ----------------------------------------------------------------------------------
    path('votacao/administradores/', views.Administarion_View_Votacao.as_view(), name = 'votacao'),


]


