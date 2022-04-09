from django.urls import path
from . import views


app_name = 'dashboard'



urlpatterns = [

    path('dashboard/', views.Dashboard_View.as_view(), name = 'manager'),
    path('dashboard/unidade/<id_unidade>/financeiro/',views.Financeiro_View.as_view(), name = 'financeiro_unidade'),
    path('dashboard/<id_unidade>/ocorrencia/',views.Ocorrencia.as_view(), name = 'ocorrencias'),
]





