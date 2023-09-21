from django.contrib import admin
from .models import Colindancias, DatosAvaluos, DatosTerceros, DocumentoPropiedad, Edificacion, EdificioVerde, Expedientes_CEDOC, FoliosReales, InstitucionesOcupantes, NumeroPlano, Ocupaciones, Task, TramitesDisposicion

# Define TabularInline para cada modelo

class FoliosRealesInline(admin.TabularInline):
    model = FoliosReales

class Expedientes_CEDOCInline(admin.TabularInline):
    model = Expedientes_CEDOC

class NumeroPlanoInline(admin.TabularInline):
    model = NumeroPlano

class EdificacionInline(admin.TabularInline):
    model = Edificacion
    

class EdificioVerdeInline(admin.TabularInline):
    model = EdificioVerde
    
class DocumentoPropiedadInline(admin.TabularInline):
    model = DocumentoPropiedad
    
class DatosAvaluosInline(admin.TabularInline):
    model = DatosAvaluos
    

class OcupacionesInline(admin.TabularInline):
    model = Ocupaciones
    
  
class DatosTercerosInline(admin.TabularInline):
    model = DatosTerceros

class ColindanciasInline(admin.TabularInline):
    model = Colindancias

class TramitesDisposicionInline(admin.TabularInline):
    model = TramitesDisposicion


# Agrega más TabularInline para otros modelos aquí...

# Define una clase personalizada para mostrar todos los modelos en una sola página
class AllModelsAdmin(admin.ModelAdmin):
    inlines = [
        FoliosRealesInline,
        Expedientes_CEDOCInline,
        NumeroPlanoInline,
        EdificacionInline,
        EdificioVerdeInline,
        DocumentoPropiedadInline,
        DatosAvaluosInline,
        OcupacionesInline,
        DatosTercerosInline,
        ColindanciasInline,
        TramitesDisposicionInline
        
        # Agrega más TabularInline aquí para otros modelos...
    ]

    readonly_fields = ('created','updated' )
    verbose_name = 'Tareas'
    list_display = ('NombreInmueble','rfi','user','pais', 'entidad_federativa', 'datecompleted')
    search_fields = ('rfi', 'user', 'pais')
    list_filter = ('user', 'pais')

# Registra la clase personalizada que contiene todos los modelos
admin.site.register(Task, AllModelsAdmin)
