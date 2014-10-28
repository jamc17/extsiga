from django.conf.urls import patterns, include, url

from combustible import views

urlpatterns = patterns('',
    url(r'^getContratosSiga$', views.getContratosSiga, name='getContratosSiga'),
    url(r'^getDetalleContratoSiga$', views.getDetalleContratoSiga, name='getDetalleContratoSiga'),
    url(r'^filtrosContratosSiga$', views.filtrosContratosSiga, name='filtrosContratosSiga'),
    url(r'^importarContratosSiga$', views.importarContratosSiga, name='importarContratosSiga'),
    url(r'^importarProveedoresSiga$', views.importarProveedoresSiga, name='importarProveedoresSiga'),
    url(r'^defineProveedoresContratos$', views.defineProveedoresContratos, name='defineProveedoresContratos'),
    url(r'^getEjecutoras$', views.getEjecutoras, name='getEjecutoras'),
    url(r'^getDetalleEjecutora$', views.getDetalleEjecutora, name='getDetalleEjecutora'),
    
    
)