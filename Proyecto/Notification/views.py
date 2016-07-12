from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from .models import Notification
from .forms import MensajeFormPaciente, MensajeFormDoctor
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from Corazon.models import Doctor, Paciente

# Create your views here.


def showNotificacion(request, id_noti):
	n = Notification.objects.get(id=id_noti)
	return render(request, "notification.html", {"notification" : n})


def deleteNotificacion(request, id_noti):
	n = Notification.objects.get(id=id_noti)
	n.leido = True
	n.save()
	return HttpResponseRedirect('/notification/verMensajes')


def showALLNotification(request):
	notification = Notification.objects.filter(user1=request.user)
	context = {
		"notification": notification,
		}
	return render(request, "verMensajes.html",context)


def enviarMensaje(request):
	user = request.user
	if user.groups.filter(name='Pacientes').exists():
		doctorid = Doctor.objects.get(id = user.paciente.doctor1.id)
		userid = doctorid.usuario.id
		form = MensajeFormPaciente(request.POST or None, userid=userid)
	if user.groups.filter(name='Doctores').exists():
		doctorid2 = user.doctor.id
		form = MensajeFormDoctor(request.POST or None, userid=doctorid2)
	
	context = {
		"titulo": "Enviar Mensaje",
		"form": form }


	if form.is_valid():
		instancia = form.save(commit=False)#instancia es un objeto Notificacion
		
		instancia.user_envio = "%s %s (%s)" %(user.first_name, user.last_name, user.username)
		print "FUERA DEL IF"
		print instancia.user_envio
		instancia.save()
		messages.add_message(request, messages.INFO, 'Mensaje enviado con exito.' )#MESSAGES DESPUES DE AGREGAR PAC

		context = {
			"titulo": "Enviar otro mensaje."
		}

	return render(request, "registrar.html", context)
