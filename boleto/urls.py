from financeiro.models import Pagamento
from django.urls import path
from . import views


app_name = "boletos"




urlpatterns = [

    path('boletos/', views.Boleto_View.as_view(), name = 'manager'), 
    path('boleto/<numero_documento>/print/', views.Print_boleto.as_view(), name = 'print'), 
    path('boleto/<pk>/pagamento/', views.Boleto_Pagamento.as_view(), name = 'boleto_pagamento'), 
    path('pagamento/<pk>/',views.Pagamento_View.as_view(), name = 'pagamentos'),       

]


