from django.urls import path
from . import views




app_name = 'moradores'



urlpatterns = [
    
    #-------------------------------- Moradores -----------------------------------------------

    path('manager/', views.Manager_Moradores_View.as_view(), name = 'manager'),
    path('<int:pk>/details/',views.Moradores_DetailView.as_view(), name = 'details'),
    path('adicionar/moradores/',views.Adicionar_Morador.as_view(), name = 'adicionar'),
    path('updated/<pk>/', views.morador_update, name = 'updated_view'),
    path('updated/<pk>/moradores', views.Morador_Update_View.as_view(), name = 'updated'),

    #--------------------------------- Veiculos -----------------------------------------------

    path('veiculos/manager/',views.Veiculos_View.as_view(), name = 'veiculos'),
    path('adicionar/veiculo/',views.Adicionar_Veiculo.as_view(), name = 'adicionar_veiculo'),
    path('details/<veiculo_id>/veiculo/',views.Veiculos_Detail_View.as_view(), name = 'veiculo_details'),

    #--------------------------------- Animais -------------------------------------------------

    path('animais/manager/',views.Animal_View.as_view(), name = 'animais'),
    path('adicionar/animais/',views.Adicionar_Animais.as_view(), name = 'adicionar_animais'),

    #--------------------------------- Funcionario -------------------------------------------------

    path('funcionario/manager/',views.Funcionario_View.as_view(), name = 'funcionario'),
    path('adicionar/funcionarios/', views.Adicionar_funcionario.as_view(), name = 'adicionar_funcionario'),

    #---------------------------------- Anilytics ----------------------------------------------
    
    path('analytics/', views.Analytics_Moradores.as_view(), name = 'analytics'),

    
    

]








