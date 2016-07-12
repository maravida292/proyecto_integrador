# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
#Importacion de templates y otras funcionalidades
from django.views.generic import TemplateView, FormView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from Proyecto.settings import LOGIN_URL
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


#Importacion de los modelos
from eventlog.models import Log
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .models import Doctor, Paciente
from .forms import DoctorForm, PacienteForm, FormularioContactos, PacienteForm2, LoginForm, PacienteFormDOC, FormMail, userForm


#@permission_required('Corazon.delete_doctor')
@login_required
def IndexHome(request):
	if request.user.is_authenticated():
		permiso_p = False
		user = request.user
		if user.groups.filter(name='Doctor_Principal').exists():
			permiso_p = True
		return render(request, 'home.html')
	else:
		return HttpResponseRedirect('/corazon/')


def IndexDoctor(request):
	user = request.user
	if user.groups.filter(name='Doctores').exists():
		doc = Doctor.objects.get(id= user.doctor.id)
		context = { "doctor" : doc}
	else:
		print user.paciente.doctor1.id
		doc = Doctor.objects.get(id = user.paciente.doctor1.id)
		context = { "doctor" : doc}
	return render(request, "doctor.html", context)


def IndexMapa(request):    
    return render(request, 'maps.html')


def IndexNoti(request):
    return render(request, 'notifications.html')


class MostrarDoctores(ListView):
	template_name = 'administrador.html'
	model = Doctor
	context_object_name = 'doctor'#con esta variable me va a recoger todos los doctores

class MostrarPaciente(ListView):
	template_name = 'paciente.html'
	model = Paciente
	context_object_name = 'paciente'#con esta variable me va a recoger todos los pacientes


#@permission_required('Corazon.delete_doctor')
def mostrarPD(request):
	doctores = Doctor.objects.all()
	pacientes = Paciente.objects.all()
	logs = Log.objects.all()

	context = {
		"referencia": "/corazon/registrar_doc",
		"doctores": doctores,
		"pacientes": pacientes,
		"logs": logs,
		}
	return render(request, "administrador.html",context)



def RegistrarDoctor(request):
	titulo_template = "Registrar Doctor"
	if request.method == "POST":
		titulo_template = "Registrar Doctor"
		form = DoctorForm(request.POST or None)
		context = {
			"referencia": "/corazon/registrar_doc",
			"titulo": titulo_template,
			"form": form }

		if form.is_valid():
			instancia = form.save()
			perfil = Doctor()
			user = User()
			cd = form.cleaned_data
			perfil.usuario = instancia
			perfil.cedula = cd.get("cedula")
			perfil.sexo = cd.get("sexo")
			perfil.clinica = cd.get("clinica")
			perfil.telefono = cd.get("telefono")
			perfil.direccion = cd.get("direccion")
			perfil.save()
			
			user=User.objects.get(username=instancia)
			user.first_name = cd.get("nombre")	
			user.last_name = cd.get("apellido")	
			user.email = cd.get("correo")
			user.groups.add(Group.objects.get(name="Doctores"))###IMPORTANTE PARA AGREGAR AL GRUPO DE DOCTORES
			user.save() #guarda la informacion
			messages.add_message(request, messages.INFO, 'Doctor se ha registrado con exito.' )#MESSAGES DESPUES DE AGREGAR DOC
		else:
			titulo2 = "Informacion con datos incorrectos"

		form = DoctorForm()
		context = {
			"referencia": "/corazon/registrar_doc",
			"titulo": titulo_template,
			"titulo2": titulo2,
			"form" : form 
		}
		return render(request, "registrar.html", context) 

	else: #GET
		form = DoctorForm()
		context = {'form' : form, "titulo": titulo_template}
		return render(request, "registrar.html", context)



def RegistrarPaciente(request):
	form = PacienteForm(request.POST or None, request.FILES or None)
	context = {
		"titulo": "Registrar Paciente",
		"form": form }

	if form.is_valid():
		instancia = form.save(commit=False)#instancia es un objeto Paciente ;)		
		p1 = Paciente()
		cd = form.cleaned_data

		form.save()
		p1.usuario = instancia
		p1.cedula = cd.get("cedula")
		p1.sexo = cd.get("sexo")
		p1.edad = cd.get("edad")
		p1.telefono = cd.get("telefono")
		p1.estado_civil = cd.get("estado_civil")
		p1.nacionalidad = cd.get("nacionalidad")
		p1.doctor1 = cd.get("doctor1")
		p1.save()

		user=User.objects.get(username=instancia)
		user.first_name = cd.get("nombre")	
		user.last_name = cd.get("apellido")
		user.groups.add(Group.objects.get(name="Pacientes"))
		user.save()
		messages.add_message(request, messages.INFO, 'Paciente %s, agregado con exito.' %instancia )#MESSAGES DESPUES DE AGREGAR PAC

		context = {
			"titulo_ejemplo": "Gracias %s.   Agregar otro paciente." %instancia,
			"titulo": "Agregar otro paciente."
		}

	return render(request, "registrar.html", context)



def IndexPaciente(request):		#FUNCION Muestra Pacientes del doctor LOGONEADO o Muestra info del Paciente :)
	user = request.user

	if request.user.is_authenticated():
		if user.groups.filter(name='Doctores').exists():
			doc = Doctor.objects.get(id= user.doctor.id) 
			lista_paciente = doc.paciente_set.all() #LISTA DE PACIENTES DEL DOCTOR LOGONEADO
			mensaje = "Lista de pacientes:"
			context = {	"pacientes": lista_paciente, "mensaje" : mensaje,}
			pagina = "paciente.html"
			return render(request, pagina ,context)
		if user.groups.filter(name='Pacientes').exists():
			pagina = "paciente_ver.html"
			paciente1 = Paciente.objects.get(id=user.paciente.id)
			context = { "paciente" : paciente1}
			return render(request, pagina ,context)
		return redirect("administrador") #Se redirige a la url q tiene como nombre ¨administrador¨




def editPaciente(request, id_prod):
	paciente1 = Paciente.objects.get(id=id_prod)
	user1 = User.objects.get(id=paciente1.usuario.id)
	titulo = "Paciente"
	info = "Iniciando"

	if request.method == "POST":
		form = PacienteFormDOC(request.POST,request.FILES,instance=paciente1)
		form2 = userForm(request.POST, instance=user1)
		if all([form.is_valid(), form2.is_valid()]):
			form.save()# Guardamos el objeto paciente
			form2.save()# Guardamos el objeto usuario
			info = "Correcto"
			return HttpResponseRedirect('/corazon/paciente/')
	else:
		form = PacienteFormDOC(instance=paciente1)
		form2 = userForm(instance=user1)
	context = {'form':form, 'form2':form2,'informacion':info, 'titulo':titulo}
	return render_to_response("paciente_edit.html",context,context_instance=RequestContext(request))


def editPacientDoc(request, id_prod, model, formulario):
	idPaciente = int(id_prod)
	item = model.objects.get(id=idPaciente)
	user1 = User.objects.get(id=item.usuario.id)
	titulo = "Doctor"
	info = "Iniciando"

	if request.method == "POST":
		form = formulario(request.POST, request.FILES, instance=item)
		form2 = userForm(request.POST, instance=user1)
		if all([form.is_valid(), form2.is_valid()]):
			form.save()#Guardamos objeto
			form2.save()#Guardamos objeto
			info = "Correcto"
			return HttpResponseRedirect('/corazon/paciente/')
	else:
		form = formulario(instance=item)
	context = {'form':form, 'form2':form2,'informacion':info, 'titulo':titulo}
	return render_to_response("paciente_edit.html",context,context_instance=RequestContext(request))


def deletePD(request, id_item, model):
	item_eliminar = model.objects.get(id=id_item)#Buscamos el Paciente/Doctor con ese id
	user = User.objects.get(id=item_eliminar.usuario.id)
	if request.method == 'POST':
		user.delete()
		return redirect('administrador') #Se redirige a la url q tiene como nombre ¨administrador¨
	return render(request, 'deletePD.html', {'item_eliminar':item_eliminar})


def verPacienteDeUnID(request, id_prod):
	idPaciente = int(id_prod)
	paciente1 = Paciente.objects.get(id=idPaciente)
	ctx = {'paciente':paciente1,}
	return render(request,"paciente_ver.html", ctx)

def enviarMailPac(request, id_pac):
	pac = Paciente.objects.get(id=id_pac)
	mail_destinatario = pac.usuario.email
	print mail_destinatario
	if (mail_destinatario != ""):
			print "Sii hay correo"
	titulo = ""
	if (mail_destinatario != ""):
		if request.method == 'POST':
			form = FormMail(request.POST)
			context = {	"titulo" : titulo, "form" : form }
			if form.is_valid():
				cd = form.cleaned_data
				titulo = cd['asunto']
				texto = cd['mensaje']
				#CONFIGURACION ENVIANDO MENSAJE VIA GMAIL... subject, contenido, quien lo esta mandando, lista_destinatarios
				to_admin = 'girlsbaby_213@hotmail.com'
				html_content = "Informacion recibida. <br> <br> <br> >>>>>>>>MENSAJE<<<<<<<< <br> <br> %s" %(texto)
				msg = EmailMultiAlternatives('NOTIFICACION', html_content, 'from@server.com', [mail_destinatario])
				msg.attach_alternative(html_content, 'text/html')
				msg.send()
				context = { "titulo" : "Se envio correctamente el e-mail" }
		else:	#GET
				form = FormMail()
				context = {	"titulo" : titulo, "form" : form }
	else:
		context = {	"titulo" : "El paciente no tiene correo "}
	return render(request, "formulario_contactos.html", context)


###Funcion para enviar correos electronicos del Doctor al Paciente
def contactos(request):
	titulo = ""
	if request.method == 'POST':
		form = FormularioContactos(request.POST)
		context = {	"titulo" : titulo, "form" : form }

		if form.is_valid():
			cd = form.cleaned_data
			email = cd['email']
			titulo = cd['asunto']
			texto = cd['mensaje']
			#CONFIGURACION ENVIANDO MENSAJE VIA GMAIL... subject, contenido, quien lo esta mandando, lista_destinatarios
			to_admin = 'girlsbaby_213@hotmail.com'
			html_content = "Informacion recibida. <br> <br> <br> >>>>>>>>MENSAJE<<<<<<<< <br> <br> %s" %(texto)
			msg = EmailMultiAlternatives('NOTIFICACIONES', html_content, 'from@server.com', [email])
			msg.attach_alternative(html_content, 'text/html')
			msg.send()
			context = { "titulo" : "Se envio correctamente el e-mail" }			
	else:	#GET
			form = FormularioContactos()
			context = {	"titulo" : titulo, "form" : form }
	return render(request, "formulario_contactos.html", context)


from eventlog.models import log

##FUNCION PARA EL LOGIN
def login_view(request):
	mensaje = ""
	next = request.POST.get('next', request.GET.get('next', ''))
	if request.user.is_authenticated():
		return HttpResponseRedirect("/corazon/home/")
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username, password=password)
				if usuario is not None and usuario.is_active:
					log(user=usuario, action='LOGIN', extra={"apellido": usuario.last_name, "nombre": usuario.first_name})
					login(request,usuario)
					
					if next:
						return HttpResponseRedirect(next)# a la raiz
					return HttpResponseRedirect('/corazon/home')
				else:
					mensaje = "usuario y/o password incorrecto"
		else:
			print "La url es %s" %next
			form = LoginForm()
			ctx = {'form':form,'mensaje':mensaje, 'next': next}
			return render_to_response('login.html',ctx,context_instance=RequestContext(request))


def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/corazon/')


