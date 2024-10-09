from django.contrib import admin

from MDSJSEP.models import EventosCreados
from condia.models import TareasCondia
from .models import ColindanciasIMP, DatosAvaluosIMP, DatosLlamadasInmuebles, DatosTercerosIMP, DictamenEstructuralIMP, Documento_ocupacionIMP, DocumentoPropiedadIMP, EdificacionIMP, EdificioVerdeIMP, Events, Expedientes_CEDOCIMP, FoliosRealesIMP, Inmueble, InstitucionesOcupantesIMP, MensajeIMP, NumeroPlanoIMP, OcupacionesIMP, RegistroLlamadas, TramitesDisposicionIMP

class RegistroLlamadas(admin.TabularInline):
    model = RegistroLlamadas


# Define una clase personalizada para mostrar todos los modelos en una sola página
class AllModelsLlamadas(admin.ModelAdmin):
    inlines = [
        RegistroLlamadas,
    ]

    list_display = ('NombreInmueble','rfi','edo', 'ur')
    search_fields = ('rfi', 'NombreInmueble')

from reversion.admin import VersionAdmin

# Registra la clase personalizada que contiene todos los modelos y hereda de VersionAdmin
@admin.register(DatosLlamadasInmuebles)
class LlamadasAdmin(VersionAdmin, AllModelsLlamadas):
    pass


# Inmuebles
class DictamenEstructuralInlineIMP(admin.TabularInline):
    model = DictamenEstructuralIMP

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

class MensajesInlineIMP(admin.TabularInline):
    model = MensajeIMP

# Agrega más TabularInline para otros modelos aquí...

# Define una clase personalizada para mostrar todos los modelos en una sola página
class AllModelsAdminIMP(admin.ModelAdmin):
    inlines = [
        DictamenEstructuralInlineIMP,
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
        MensajesInlineIMP,

        # Agrega más TabularInline aquí para otros modelos...
    ]

    list_display = ('NombreInmueble','rfi','pais', 'entidad_federativa')
    search_fields = ('rfi', 'NombreInmueble', 'pais')
    list_filter = ('user', 'pais')

from reversion.admin import VersionAdmin

# Registra la clase personalizada que contiene todos los modelos y hereda de VersionAdmin
@admin.register(Inmueble)
class InmuebleAdmin(VersionAdmin, AllModelsAdminIMP):
    pass




# Registra los otros modelos
admin.site.register(TareasCondia)
# Registra otros modelos aquí...

class EventsAdmin(admin.ModelAdmin):
    list_display = ('title',  'hora_inicio', 'hora_finalizacion', 'coordina')
admin.site.register(Events, EventsAdmin)

class EventosCreadosAdmin(admin.ModelAdmin):
    list_display = ('title', 'Nom_sala', 'hora_inicio', 'hora_finalizacion', 'coordina')
admin.site.register(EventosCreados, EventosCreadosAdmin)

