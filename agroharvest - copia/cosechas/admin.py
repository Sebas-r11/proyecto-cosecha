from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado, ConfiguracionAlertas

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Rol y Dativos Extra', {'fields': ('rol', 'telefono')}),
    )

admin.site.register(UsuarioPersonalizado, UsuarioAdmin)

@admin.register(ConfiguracionAlertas)
class ConfiguracionAlertasAdmin(admin.ModelAdmin):
    list_display = ('humedad_minima', 'humedad_maxima', 'ultima_actualizacion')
    fields = ('humedad_minima', 'humedad_maxima')