from django.contrib import admin
from .models import Colindancias, DatosAvaluos, DatosTerceros, DocumentoPropiedad, Edificacion, EdificioVerde, Expedientes_CEDOC, FoliosReales, InstitucionesOcupantes, NumeroPlano, Ocupaciones, Task, TramitesDisposicion

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ('created','updated' )
  verbose_name='Tareas'
  list_display = ('NombreInmueble','rfi','user','pais', 'entidad_federativa', 'datecompleted')
  search_fields = ('rfi', 'user', 'pais')
  list_filter = ('user', 'pais')
  
admin.site.register(Task, TaskAdmin)

class FoliosRealesAdmin(admin.ModelAdmin):
    list_display = ('task',  'folios_reales_data')  # Campos a mostrar en la lista
    list_filter = ('task',)  # Filtro por tarea
admin.site.register(FoliosReales, FoliosRealesAdmin)

class ExpedienteCEDOC(admin.ModelAdmin):
    list_display = ('task', 'expediente_cedoc_data')
    list_filter = ('task',)
admin.site.register(Expedientes_CEDOC,ExpedienteCEDOC)

class NoPlanoAdmin(admin.ModelAdmin):
  list_display =  ('task', 'numero_plano_data')
  list_filter = ('task',)
admin.site.register(NumeroPlano, NoPlanoAdmin)

class EdificacionAdmin(admin.ModelAdmin):
  list_display = ('task', 'nombre_edificacion')
  list_filter = ('task',)
admin.site.register(Edificacion, EdificacionAdmin)

class EdificioVerdeAdmin(admin.ModelAdmin):
  list_display = ('task', 'edificio_verde_data')
  list_filter = ('task',)
admin.site.register(EdificioVerde, EdificioVerdeAdmin)

class DocumentoPropiedadAdmin(admin.ModelAdmin):
  list_display = ('task', 'propietario_inmueble')
  list_filter = ('task',)
admin.site.register(DocumentoPropiedad, DocumentoPropiedadAdmin)

class DatosAvaluosAdmin(admin.ModelAdmin):
  list_display = ('task', 'numero_de_avaluo')
admin.site.register(DatosAvaluos, DatosAvaluosAdmin)

class OcupacionesAdmin(admin.ModelAdmin):
  list_display = ('task', 'tipo_procedimiento', 'nombre_ocupante')
admin.site.register(Ocupaciones, OcupacionesAdmin)

class InstitucionOcupanteAdmin(admin.ModelAdmin):
  list_display = ('task', 'institucion_publica_ocupante')
admin.site.register(InstitucionesOcupantes, InstitucionOcupanteAdmin)

class DatosTercerosAdmin(admin.ModelAdmin):
    list_display = ('tipo_usuario_tercero', 'beneficiario', 'nombre_beneficiario', 'rfc', 'fecha_inicio_vigencia', 'fecha_termino_vigencia', 'prorroga', 'inscripcion_folio_real_federal', 'superficie_objeto_ocupacion_metros', 'uso')
    list_filter = ('tipo_usuario_tercero', 'beneficiario')
    search_fields = ('nombre_beneficiario', 'rfc')
admin.site.register(DatosTerceros, DatosTercerosAdmin)

class ColindanciaAdmin(admin.ModelAdmin):
    list_display = ('orientacion', 'colindancia', 'medida_en_metros')
    list_filter = ('orientacion',)
    search_fields = ('orientacion', 'colindancia', 'medida_en_metros')

# Registrar el modelo y el admin personalizado
admin.site.register(Colindancias, ColindanciaAdmin)

class TramitesDisposicionAdmin(admin.ModelAdmin):
    list_display = ('tramite_disposicion', 'estatus', 'numero_de_expediente')
admin.site.register(TramitesDisposicion, TramitesDisposicionAdmin)