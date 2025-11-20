from django.contrib import admin
from .models import InmuebleCondia

@admin.register(InmuebleCondia)
class InmuebleCondiaAdmin(admin.ModelAdmin):
    list_display = ('NombreInmueble', 'descripcion', 'fecha_creacion', 'creado_por', 'estado')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('NombreInmueble', 'descripcion', 'creado_por__username')

