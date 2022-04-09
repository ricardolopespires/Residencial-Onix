from django.urls import path
from . import views




app_name = "colaboradores"





urlpatterns = [

    path('funcionarios/manager/', views.Funcionarios_Manager.as_view(), name = 'manager'),
    path('funcionarios/adicionar/', views.Adicionar_funcionario.as_view(), name = 'adicionar' ),
    path('funcionario/<int:pk>/details',views.Funcionarios_Details.as_view(), name = 'details'),

    path('funcionario/avaliacao/<int:pk>/details', views.Avalicao_details.as_view(), name = 'avaliacao_details'),
    
]
