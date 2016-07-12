from __future__ import unicode_literals

from django.db import models
#from django.contrib.auth.models import User
from Corazon.models import Paciente

class Ubicacion(models.Model):
	nombre = models.CharField(max_length=200)
	lat = models.CharField(max_length=50)
	lng = models.CharField(max_length=50)
	fecha = models.DateTimeField(auto_now_add=True)
	pac1 = models.ForeignKey(Paciente, on_delete=models.CASCADE)

	def __unicode__(self):
		return self.nombre


