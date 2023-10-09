from django.contrib import admin
from .models import Colindancias, ColindanciasIMP, DatosAvaluos, DatosAvaluosIMP, DatosTerceros, DatosTercerosIMP, Documento_ocupacion, Documento_ocupacionIMP, DocumentoPropiedad, DocumentoPropiedadIMP, Edificacion, EdificacionIMP, EdificioVerde, EdificioVerdeIMP, Expedientes_CEDOC, Expedientes_CEDOCIMP, FoliosReales, FoliosRealesIMP, Inmueble, InstitucionesOcupantes, InstitucionesOcupantesIMP, Mensaje, NumeroPlano, NumeroPlanoIMP, Ocupaciones, OcupacionesIMP, Task, Task_Condia, TramitesDisposicion, TramitesDisposicionIMP

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




class FoliosRealesInlineIMP(admin.TabularInline):
    model = FoliosRealesIMP

class Expedientes_CEDOCInlineIMP(admin.TabularInline):
    model = Expedientes_CEDOCIMP

class NumeroPlanoInlineIMP(admin.TabularInline):
    model = NumeroPlanoIMP

class EdificacionInlineIMP(admin.TabularInline):
    model = EdificacionIMP
    

class EdificioVerdeInlineIMP(admin.TabularInline):
    model = EdificioVerdeIMP
    
class DocumentoPropiedadInlineIMP(admin.TabularInline):
    model = DocumentoPropiedadIMP
    
class DatosAvaluosInlineIMP(admin.TabularInline):
    model = DatosAvaluosIMP
    
class DocumentoOcupacionInlineIMP(admin.TabularInline):
    model = Documento_ocupacionIMP

class OcupacionesInlineIMP(admin.TabularInline):
    model = OcupacionesIMP
    
  
class DatosTercerosInlineIMP(admin.TabularInline):
    model = DatosTercerosIMP

class ColindanciasInlineIMP(admin.TabularInline):
    model = ColindanciasIMP

class TramitesDisposicionInlineIMP(admin.TabularInline):
    model = TramitesDisposicionIMP

class InstitucionesOcupantesInlineIMP(admin.TabularInline):
    model = InstitucionesOcupantesIMP


# Agrega más TabularInline para otros modelos aquí...

# Define una clase personalizada para mostrar todos los modelos en una sola página
class AllModelsAdminIMP(admin.ModelAdmin):
    inlines = [
        FoliosRealesInlineIMP,
        NumeroPlanoInlineIMP,
        Expedientes_CEDOCInlineIMP,
        ColindanciasInlineIMP,
        EdificacionInlineIMP,
        EdificioVerdeInlineIMP,
        DocumentoPropiedadInlineIMP,
        DocumentoOcupacionInlineIMP,
        InstitucionesOcupantesInlineIMP,
        DatosTercerosInlineIMP,
        DatosAvaluosInlineIMP,
        OcupacionesInlineIMP,
        TramitesDisposicionInlineIMP,
        
        
        
        # Agrega más TabularInline aquí para otros modelos...
    ]

    list_display = ('NombreInmueble','rfi','pais', 'entidad_federativa')
    search_fields = ('rfi', 'NombreInmueble', 'pais')
    list_filter = ('user', 'pais')

# Registra la clase personalizada que contiene todos los modelos
admin.site.register(Inmueble, AllModelsAdminIMP)