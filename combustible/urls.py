from django.conf.urls import patterns, include, url

from combustible import views

urlpatterns = patterns('',
    url(r'^listContratosSiga$', views.listContratosSiga, name='listContratosSiga'),
    url(r'^filtrosContratosSiga$', views.filtrosContratosSiga, name='filtrosContratosSiga'),
    url(r'^importarContratosSiga$', views.importarContratosSiga, name='importarContratosSiga'),
    url(r'^importarProveedoresSiga$', views.importarProveedoresSiga, name='importarProveedoresSiga'),
    url(r'^defineProveedoresContratos$', views.defineProveedoresContratos, name='defineProveedoresContratos'),
    
)