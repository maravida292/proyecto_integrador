from django.conf.urls import patterns, url
from gmaps import views

urlpatterns = [
	url(r'^ver/', views.verMapa, name='verMapa'),
]