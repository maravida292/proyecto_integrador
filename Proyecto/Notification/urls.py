from django.conf.urls import patterns, url
from Notification import views


urlpatterns = [
	url(r'^verMensajes/', views.showALLNotification, name='ver_Mensajes'),
	url(r'^ver/(?P<id_noti>.*)/', views.showNotificacion, name='ver_notification'),
	url(r'^delete/(?P<id_noti>.*)/', views.deleteNotificacion, name='delete_notification'),
	url(r'^enviarMensaje/', views.enviarMensaje, name='enviar_Mensaje'),
]