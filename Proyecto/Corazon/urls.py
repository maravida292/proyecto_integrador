from django.conf.urls import patterns, url
from django.conf.urls.static import static
from Corazon import views
from .views import MostrarDoctores, MostrarPaciente
from .models import Doctor, Paciente
from .forms import DoctorForm2, Doctor2Form



urlpatterns = [
  #   url(r'^$' , 'django.contrib.auth.views.login',
		# {'template_name':'login.html'}, name='login'),

  #   url(r'^cerrar/$' , 'django.contrib.auth.views.logout_then_login',
		#  name='logout'),
	url(r'^$', views.login_view, name='login'),
	url(r'^cerrar/$', views.logout_view, name='logout'),

#INDEX VIEW

	url(r'^home/', views.IndexHome, name='home'),	
	url(r'^doctor/', views.IndexDoctor, name='doctor'),
	url(r'^mapa/', views.IndexMapa, name='mapa'),
	url(r'^noti/', views.IndexNoti, name='noti'),
	

	url(r'^registrar_doc/$', views.RegistrarDoctor, name='registrar_doc'),
	url(r'^registrar_pac/$', views.RegistrarPaciente, name='registrar_pac'),

#	url(r'^detalle_doctor/$', views.mostrarPD, {'model':'Doctor','plantilla': 'bienvenidos.html'}),
#	url(r'^detalle_paciente/$', views.mostrarPD, {'model':'Paciente','plantilla': 'bienvenidos.html'}),

	url(r'^administrador/', views.mostrarPD, name = 'administrador'),
	url(r'^paciente/$', views.IndexPaciente , name = 'paciente'),#Simbolo dolar sirve para decirla a la URL que va a existir mas extensiones
	url(r'^contactos/', views.contactos, name ='contactos'),
	url(r'^ver/paciente/(?P<id_prod>.*)/$', views.verPacienteDeUnID, name= 'ver_paciente'),
	url(r'^edit/paciente/(?P<id_prod>.*)/', views.editPaciente, name= 	'editar_paciente'),
	url(r'^eliminar/doctor/(?P<id_item>.*)/', views.deletePD, {'model': Doctor}, name= 'delete_D'),
	url(r'^eliminar/paciente/(?P<id_item>.*)/', views.deletePD, {'model': Paciente}, name= 'delete_P'),
	url(r'^mail/(?P<id_pac>.*)/', views.enviarMailPac, name= 'mail_pac'),
	
	#En la sigt URL se envia el modelo, formulario y x medio de la url se trae el id correspondiente
	url(r'^edit/doctor/(?P<id_prod>.*)/', views.editPacientDoc, {'model': Doctor, 'formulario' : Doctor2Form}),


]
