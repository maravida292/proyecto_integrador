from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Notification(models.Model):
	titulo = models.CharField(max_length=256)
	mensaje = models.TextField()
	leido = models.BooleanField(default=False)
	user1 = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha = models.DateTimeField(auto_now=True)
	user_envio = models.CharField(max_length=50, blank=True, null=True)

	def __unicode__(self):		
		return '%s %s' % (self.user1.username, self.titulo)
