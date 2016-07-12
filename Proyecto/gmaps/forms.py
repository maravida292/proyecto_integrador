from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ubicacion


class UbicacionForm(ModelForm):
	class Meta:
		model = Ubicacion