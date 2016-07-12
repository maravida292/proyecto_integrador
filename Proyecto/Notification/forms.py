from django import forms
from django.contrib.auth.models import User
from .models import Notification
from Corazon.models import Doctor, Paciente

class MensajeFormPaciente(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		userid = kwargs.pop('userid')
		super(MensajeFormPaciente, self).__init__(*args, **kwargs)
		self.fields['user1'] = forms.ModelChoiceField(required=False, queryset=User.objects.filter(id=userid), label='Doctor')

	class Meta:
		model   = Notification
		fields = ['user1','titulo','mensaje']
		exclude = {'fecha','leido','user_envio'}


class MensajeFormDoctor(forms.ModelForm):#Doctor quiera enviar msj a sus pacientes

	def __init__(self, *args, **kwargs):
		userid = kwargs.pop('userid')
		super(MensajeFormDoctor, self).__init__(*args, **kwargs)
		self.fields['user1'] = forms.ModelChoiceField(required=False, queryset=User.objects.filter(paciente__doctor1__id=userid), label='Doctor')

	class Meta:
		model   = Notification
		fields = ['user1','titulo','mensaje']
		exclude = {'fecha','leido','user_envio'}