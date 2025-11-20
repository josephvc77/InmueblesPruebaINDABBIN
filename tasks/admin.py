from django.contrib import admin
from django.utils.html import format_html

from MDSJSEP.models import EventosCreados
# from condia.models import TareasCondia  # Modelo no existe, comentado
from .models import Archivo, ColindanciasIMP, Comentario, DatosAvaluosIMP, DatosLlamadasInmuebles, DatosTercerosIMP, DictamenEstructuralIMP, Documento_ocupacionIMP, DocumentoPropiedadIMP, EdificacionIMP, EdificioVerdeIMP, Expedientes_CEDOCIMP, FoliosRealesIMP, Inmueble, InstitucionesOcupantesIMP, NumeroPlanoIMP, Observacion, OcupacionesIMP, RegistroLlamadas, TramitesDisposicionIMP, HistorialUsoInmueble

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

class ObservacionesInlineIMP(admin.TabularInline):
    model = Observacion
    extra = 0
    fields = ('texto', 'usuario', 'fecha_creacion')
    readonly_fields = ('fecha_creacion',)
    
class ArchivosInlineIMP(admin.TabularInline):
    model = Archivo
    extra = 0
    fields = ('archivo', 'descripcion', 'fecha_subida')
    readonly_fields = ('fecha_subida',)

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
        ObservacionesInlineIMP,
        ArchivosInlineIMP,

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
# admin.site.register(TareasCondia)  # Modelo no existe, comentado
# Registra otros modelos aquí...


class EventosCreadosAdmin(admin.ModelAdmin):
    list_display = ('title', 'Nom_sala', 'hora_inicio', 'hora_finalizacion', 'coordina')
admin.site.register(EventosCreados, EventosCreadosAdmin)


@admin.register(HistorialUsoInmueble)
class HistorialUsoInmuebleAdmin(admin.ModelAdmin):
    list_display = ('inmueble', 'usuario', 'accion', 'fecha_hora', 'ip_address')
    list_filter = ('accion', 'fecha_hora', 'inmueble')
    search_fields = ('inmueble__NombreInmueble', 'usuario__username', 'descripcion')
    readonly_fields = ('fecha_hora',)
    date_hierarchy = 'fecha_hora'
    ordering = ('-fecha_hora',)


@admin.register(Observacion)
class ObservacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_inmueble', 'get_texto_preview', 'usuario', 'fecha_creacion', 'get_comentarios_count')
    list_filter = ('fecha_creacion', 'usuario', 'task')
    search_fields = ('texto', 'task__NombreInmueble', 'usuario__username', 'usuario__first_name', 'usuario__last_name')
    readonly_fields = ('fecha_creacion', 'get_inmueble_detail', 'get_comentarios_count')
    date_hierarchy = 'fecha_creacion'
    ordering = ('-fecha_creacion',)
    
    fieldsets = (
        ('Información de la Observación', {
            'fields': ('task', 'texto', 'usuario', 'fecha_creacion')
        }),
        ('Relaciones', {
            'fields': ('get_inmueble_detail', 'get_comentarios_count'),
            'classes': ('collapse',)
        }),
    )
    
    def get_inmueble(self, obj):
        """Obtiene el inmueble"""
        if obj.task:
            return obj.task.NombreInmueble or f"Inmueble ID: {obj.task.id}"
        return "N/A"
    get_inmueble.short_description = 'Inmueble'
    get_inmueble.admin_order_field = 'task__NombreInmueble'
    
    def get_inmueble_detail(self, obj):
        """Muestra información detallada del inmueble"""
        if obj.task:
            inmueble = obj.task
            return format_html(
                '<strong>Inmueble:</strong> {}<br>'
                '<strong>RFI:</strong> {}<br>'
                '<strong>ID:</strong> {}<br>'
                '<a href="/admin/tasks/inmueble/{}/change/" target="_blank">Ver en Admin</a>',
                inmueble.NombreInmueble or 'Sin nombre',
                inmueble.rfi or 'N/A',
                inmueble.id,
                inmueble.id
            )
        return "No hay inmueble asociado"
    get_inmueble_detail.short_description = 'Detalles del Inmueble'
    
    def get_texto_preview(self, obj):
        """Muestra un preview del texto de la observación"""
        if obj.texto:
            if len(obj.texto) > 100:
                return obj.texto[:100] + "..."
            return obj.texto
        return "Sin texto"
    get_texto_preview.short_description = 'Texto (Preview)'
    get_texto_preview.admin_order_field = 'texto'
    
    def get_comentarios_count(self, obj):
        """Muestra el número de comentarios"""
        count = obj.comentarios.count()
        if count > 0:
            return format_html(
                '<a href="/admin/tasks/comentario/?observacion__id__exact={}" target="_blank">{} comentario(s)</a>',
                obj.id,
                count
            )
        return "0 comentarios"
    get_comentarios_count.short_description = 'Comentarios'
    
    def get_queryset(self, request):
        """Optimizar las consultas con select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('task', 'usuario').prefetch_related('comentarios')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_inmueble', 'get_observacion_preview', 'get_comentario_preview', 'usuario', 'fecha_creacion')
    list_filter = ('fecha_creacion', 'usuario', 'observacion__task')
    search_fields = ('texto', 'observacion__texto', 'observacion__task__NombreInmueble', 'usuario__username', 'usuario__first_name', 'usuario__last_name')
    readonly_fields = ('fecha_creacion', 'get_inmueble_detail', 'get_observacion_detail')
    date_hierarchy = 'fecha_creacion'
    ordering = ('-fecha_creacion',)
    
    fieldsets = (
        ('Información del Comentario', {
            'fields': ('texto', 'usuario', 'fecha_creacion')
        }),
        ('Relaciones', {
            'fields': ('observacion', 'get_inmueble_detail', 'get_observacion_detail'),
            'classes': ('collapse',)
        }),
    )
    
    def get_inmueble(self, obj):
        """Obtiene el inmueble a través de la observación"""
        if obj.observacion and obj.observacion.task:
            return obj.observacion.task.NombreInmueble or f"Inmueble ID: {obj.observacion.task.id}"
        return "N/A"
    get_inmueble.short_description = 'Inmueble'
    get_inmueble.admin_order_field = 'observacion__task__NombreInmueble'
    
    def get_inmueble_detail(self, obj):
        """Muestra información detallada del inmueble"""
        if obj.observacion and obj.observacion.task:
            inmueble = obj.observacion.task
            return format_html(
                '<strong>Inmueble:</strong> {}<br>'
                '<strong>RFI:</strong> {}<br>'
                '<strong>ID:</strong> {}<br>'
                '<a href="/admin/tasks/inmueble/{}/change/" target="_blank">Ver en Admin</a>',
                inmueble.NombreInmueble or 'Sin nombre',
                inmueble.rfi or 'N/A',
                inmueble.id,
                inmueble.id
            )
        return "No hay inmueble asociado"
    get_inmueble_detail.short_description = 'Detalles del Inmueble'
    
    def get_observacion_preview(self, obj):
        """Muestra un preview del texto de la observación"""
        if obj.observacion and obj.observacion.texto:
            texto = obj.observacion.texto
            if len(texto) > 100:
                return texto[:100] + "..."
            return texto
        return "Sin observación"
    get_observacion_preview.short_description = 'Observación (Preview)'
    get_observacion_preview.admin_order_field = 'observacion__texto'
    
    def get_observacion_detail(self, obj):
        """Muestra información detallada de la observación"""
        if obj.observacion:
            obs = obj.observacion
            usuario_obs = obs.usuario.get_full_name() if obs.usuario and hasattr(obs.usuario, 'get_full_name') else (obs.usuario.username if obs.usuario else 'N/A')
            fecha_str = obs.fecha_creacion.strftime('%d/%m/%Y %H:%M') if obs.fecha_creacion else 'N/A'
            texto_preview = (obs.texto[:200] + '...') if obs.texto and len(obs.texto) > 200 else (obs.texto or 'Sin texto')
            return format_html(
                '<strong>ID Observación:</strong> {}<br>'
                '<strong>Usuario:</strong> {}<br>'
                '<strong>Fecha:</strong> {}<br>'
                '<strong>Texto:</strong> {}<br>'
                '<a href="/admin/tasks/observacion/{}/change/" target="_blank">Ver Observación Completa</a>',
                obs.id,
                usuario_obs,
                fecha_str,
                texto_preview,
                obs.id
            )
        return "No hay observación asociada"
    get_observacion_detail.short_description = 'Detalles de la Observación'
    
    def get_comentario_preview(self, obj):
        """Muestra un preview del comentario"""
        if obj.texto:
            if len(obj.texto) > 80:
                return obj.texto[:80] + "..."
            return obj.texto
        return "Sin texto"
    get_comentario_preview.short_description = 'Comentario (Preview)'
    get_comentario_preview.admin_order_field = 'texto'
    
    def get_queryset(self, request):
        """Optimizar las consultas con select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('observacion', 'observacion__task', 'usuario')

