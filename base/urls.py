from django.conf.urls import patterns, url

from base import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
    url(r'^header$', views.header, name='header'),
    url(r'^center$', views.center, name='center'),
    url(r'^footer$', views.footer, name='footer'),
    url(r'^mainMenu$', views.mainMenu, name='mainMenu'),
)