"""Onix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from contato.forms import NewletterForm
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
#from .views import CondominioViewSet
#from rest_framework import routers
#from moradores.admin import moradores_admin_site


admin.site.site_header = "Condomínio Residencial Ônix Admin"
admin.site.site_title = "Condomínio Residencial Ônix Admin Portal"
admin.site.index_title = "Bem Vindo ao Portal do Condomínio Residencial Ônix "


# Routers provide an easy way of automatically determining the URL conf.
#router = routers.DefaultRouter()
#router.register(r'condominio', CondominioViewSet)

urlpatterns = [

    path('',views.IndexView.as_view(), name ='index'),
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    #path('moradores/admin/', moradores_admin_site.urls),
    path('sobre-nos/',views.About_View.as_view(), name = 'about'),
    path('servico/',views.Servicos_View.as_view(), name = 'servicos'),
    path('projetos/',views.Projetos_View.as_view(), name = 'projetos'),
    path('contato/',include('contato.urls', namespace = 'contato')),
    path('newletter/',views.Newletter.as_view(), name = 'newletter'),

    #------------------------------- Api -----------------------------------------------
    #path('api-auth/', include('rest_framework.urls')),
    #path('', include(router.urls)),



    #------------------------- Dashboard  -----------------------------------------------
    path('', include('dashboard.urls', namespace = 'dashboard')),

    #------------------------- management  ------------------------------------------
    path('management/', include('management.urls', namespace = 'management')),
    path('administration/', include('administration.urls', namespace = 'administration')),
    path('condominio/', include('condominio.urls', namespace = 'condominio')),
    path('financeiro/', include('financeiro.urls', namespace = 'financeiro')),
    path('moradores/',include('moradores.urls', namespace  = 'moradores')),
    path('colaboardores/', include('colaboradores.urls', namespace = 'colaboradores')),
    #path('fornecedores/', include('fornecedores.urls', namespace = 'fornecedores')),
    path('boletos/',include('boleto.urls', namespace = 'boletos')),
    path('manutencao/', include('manutencao.urls', namespace = 'manutencao')),
    




    #------------------------- Management  ----------------------------------------------

    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



