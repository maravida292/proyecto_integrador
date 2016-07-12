from django.contrib import admin

#EMPIEZO AQUI
from .models import Doctor, Paciente


class DoctorAdmin(admin.ModelAdmin):
	list_display = ('id','usuario', 'cedula', 'clinica')#como se muestra las columnas
	search_fields = ('usuario__username', 'cedula')#filtrado de Doctores por nombre de usuario y cedula
	#form = Doctor2Form
	list_editable = ('usuario', 'clinica')

class PacienteAdmin(admin.ModelAdmin):
	list_display = ('id','usuario','__unicode__', 'cedula', 'edad')
	list_filter = ('doctor1',)
	list_editable = ('usuario', 'edad')

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Paciente, PacienteAdmin)

#Instancia una clase AdminSite y registra cada uno de los modelos en la clase ModelAdmin
#Instancia una clase AdminSite y registra cada uno de los modelos en la clase ModelAdmin
#Apunta la instancia AdminSite a tu URLconf.
