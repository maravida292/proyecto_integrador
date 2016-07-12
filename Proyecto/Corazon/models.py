from __future__ import unicode_literals
from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from eventlog.models import log
from .validators import validacion_10digit, validacion_esDigito


def url(self, filename):
	ruta = "Doctor/%s/%s" %(self.usuario.username,filename)
	return ruta

def url2(self, filename):
	ruta = "Paciente/%s/%s" %(self.usuario.username,filename)
	return ruta

class Doctor(models.Model):

	SEX = (('M', 'Masculino'),('F', 'Femenino'),)
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	cedula = models.CharField(max_length=10, validators=[validacion_10digit, validacion_esDigito])
	sexo = models.CharField(max_length=2, choices=SEX)
	clinica = models.CharField(max_length=30, blank=True)
	telefono = models.CharField(max_length=10, null=True, blank=True, validators=[validacion_esDigito])#atributos de fecha y numericos no aceptan cadena vacia(blank=true)
	direccion = models.CharField(max_length=50,null=True, blank=True)
	foto = models.ImageField(upload_to=url, blank=True, null=True)

	class Meta:
		permissions = (
			("send_mail", "Puede enviar mails"),
		)

	def __unicode__(self):# __str__ para python3
		return self.usuario.username

	def save(self, *args, **kwargs):
		if not self.id:
			log(user=self.usuario, action='ADD_DOCTOR', extra={"cedula": self.cedula})
		else:
			log(user = self.usuario, action='UPDATE_DOCTOR', extra={"cedula": self.cedula})

		super(Doctor, self).save(args, kwargs)



class Paciente(models.Model):
	CIVIL = ((u'S', u'Soltero'),(u'C', u'Casado'),(u'D', u'Divorsiado'),(u'V', u'Viudo'),)
	SEX = ((u'M', u'Mujer'),(u'H', u'Hombre'),)
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	cedula = models.CharField(max_length=10, validators=[validacion_10digit, validacion_esDigito])
	sexo = models.CharField(max_length=2, choices=SEX)
	edad = models.CharField(max_length=3, validators=[validacion_esDigito])
	telefono = models.CharField(max_length=10, null=True, blank=True, validators=[validacion_esDigito])
	estado_civil = models.CharField(max_length=2, choices=CIVIL, blank=True)
	nacionalidad = models.CharField(max_length=20, blank=True)
	foto = models.ImageField(upload_to=url2, blank=True, null=True)
	doctor1 = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		permissions = (
			("ver_perfil", "Pueden ver su perfil"),
		)

	def __unicode__(self):
		return '%s %s' % (self.usuario.first_name, self.usuario.last_name)

	def save(self, *args, **kwargs):
		if not self.id:
			log(user=self.usuario, action='ADD_PACIENTE', extra={"cedula": self.cedula,"Usuario": self.usuario.username })
		else:
			log(user = self.usuario, action='UPDATE_PACIENTE', extra={"cedula": self.cedula,"Usuario": self.usuario.username})

		super(Paciente, self).save(args, kwargs)

def _nombre_completo(self):
	return '%s %s' % (self.usuario.first_name, self.usuario.last_name)
     #"Retorna el nombre completo de una persona." 
