from django.core.exceptions import ValidationError


def validacion_10digit(value):
	if len(value) < 10:
		raise ValidationError("Este campo debe tener 10 digitos.")

def validacion_esDigito(value):
	if not(value.isdigit()):
		raise ValidationError("Ingrese numeros.")
