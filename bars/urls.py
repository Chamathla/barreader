from django.conf.urls import patterns, url
from bars import final_app
from bars import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^city/$', views.city, name='city'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
	url(r'^maps/$',final_app.maps, name='maps'),
)

