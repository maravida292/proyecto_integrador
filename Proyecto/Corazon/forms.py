# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor, Paciente


#Piensa en las clases Field como las encargadas de la logica de 
#validacion , mientras que los widgets se encargan de la logica de presentacion

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
SEXO = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)
CIVIL = ((u'S', u'Soltero'),(u'C', u'Casado'),(u'D', u'Divorsiado'),(u'V', u'Viudo'),)


class DoctorForm(UserCreationForm):
	nombre = forms.CharField(max_length=30,widget=forms.TextInput())
	apellido = forms.CharField(max_length=30,widget=forms.TextInput())	
	cedula = forms.CharField(max_length=10, label=u'Cédula')
	sexo = forms.CharField(max_length=3,
        widget=forms.Select(choices=SEXO),)
	clinica = forms.CharField(max_length=30, label=u'Clínica',widget=forms.TextInput())
	telefono = forms.CharField(max_length=10, label=u'Teléfono',widget=forms.TextInput())
	direccion = forms.CharField(max_length=50, label=u'Dirección',widget=forms.TextInput())
	correo = forms.EmailField(max_length=40, label='Correo Electronico', 
		widget=forms.TextInput())
	#direccion = forms.CharField(widget=forms.Textarea, label=u'Dirección')
	#cumple = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))

	def clean_cedula(self):
		cedula = self.cleaned_data.get('cedula')
		if not(cedula.isdigit()):
			raise forms.ValidationError("Ingrese numeros.")
		if len(cedula) < 10:
			raise forms.ValidationError("La cedula debe tener 10 digitos.")
		return cedula

	def clean_telefono(self):
		telefono = self.cleaned_data.get('telefono')
		if not(telefono.isdigit()):
			raise forms.ValidationError("Por favor ingresar el telefono correcta.")
		return telefono



class PacienteForm(UserCreationForm):
	nombre = forms.CharField(max_length=30,widget=forms.TextInput())
	apellido = forms.CharField(max_length=30,widget=forms.TextInput())	
	cedula = forms.CharField(max_length=10, label=u'Cédula',widget=forms.TextInput())
	sexo = forms.CharField(max_length=3,
        widget=forms.Select(choices=SEXO),)
	edad = forms.CharField(max_length=3,widget=forms.TextInput())
	estado_civil = forms.CharField(max_length=2,
        widget=forms.Select(choices=CIVIL),)
	telefono = forms.CharField(max_length=10, label=u'Teléfono',widget=forms.TextInput())
	correo = forms.EmailField(max_length=40, label='Correo Electronico', 
		widget=forms.TextInput())
	nacionalidad = forms.CharField(max_length=40, required=False,widget=forms.TextInput())
	doctor1 = forms.ModelChoiceField(queryset=Doctor.objects.all())

	def clean_cedula(self):
		cedula = self.cleaned_data.get('cedula')
		if not(cedula.isdigit()):
			raise forms.ValidationError("Ingrese numeros.")
		if len(cedula) < 10:
			raise forms.ValidationError("La cedula debe tener 10 digitos.")
		return cedula

	def clean_edad(self):
		edad = self.cleaned_data.get('edad')
		if not(edad.isdigit()):
			raise forms.ValidationError("Por favor ingresar la edad correcta.")
		if edad<=0:
			raise forms.ValidationError("Ingresar la edad correctamente.")
		return edad

	def clean_telefono(self):
		telefono = self.cleaned_data.get('telefono')
		if not(telefono.isdigit()):
			raise forms.ValidationError("Por favor ingresar el telefono correcta.")
		return telefono


class Doctor2Form(forms.ModelForm):
	class Meta:
		model = Doctor
		fields = ['sexo','clinica','telefono','direccion']

class userForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name','last_name','email']
		exclude = {'password', 'last_login', 'is_superuser', 'username'}



class FormularioContactos(forms.Form):#Formulario para envio de mails
	asunto = forms.CharField()
	email = forms.EmailField(required=False, label='Correo electronico')
	mensaje = forms.CharField(widget=forms.Textarea)


class FormMail(forms.Form):#Formulario para envio de mails
	asunto = forms.CharField()
	mensaje = forms.CharField(widget=forms.Textarea)


class PacienteForm2(forms.ModelForm):
	class Meta:
		model   = Paciente
		exclude = {'usuario'}


class PacienteFormDOC(forms.ModelForm):

	# def __init__(self, *args, **kwargs):
	# 	super(PacienteFormDOC, self).__init__(*args, **kwargs)
	# 	self.fields['cedula'].widget.attrs['disabled'] = 'disabled' 

	class Meta:
		model   = Paciente
		fields = ['sexo','edad','telefono','estado_civil', 'nacionalidad', 'foto']
		exclude = {'usuario', 'doctor1', 'cedula'}


class DoctorForm2(UserCreationForm):
	class Meta:
		model   = Doctor
		fields = ['usuario','sexo','clinica','telefono','direccion' ]
		exclude = {'foto'}


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(),initial='Usuario')
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))
	#password = forms.CharField(label="", widget=forms.PasswordInput(render_value=False))
