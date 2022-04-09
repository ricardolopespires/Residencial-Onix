from django.urls import path
from . import views




app_name ='manutencao'



urlpatterns = [

    path('manutencao/',views.Mantuncao_Manager.as_view(), name = 'manager'),
    path('manutencao/<manutencao_id>/item/', views.Manutencao_Item_View.as_view(), name ='item'),
    path('manutencao/agendamento/',views.Agendamento.as_view(), name = 'agendamento'),
    



]

