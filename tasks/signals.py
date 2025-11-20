from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import HistorialUsoInmueble, Inmueble, Archivo, Observacion, Comentario, DictamenEstructuralIMP, FoliosRealesIMP, NumeroPlanoIMP, Expedientes_CEDOCIMP, DocumentoPropiedadIMP


def get_client_ip(request):
    """Obtiene la dirección IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def registrar_accion(inmueble, usuario, accion, descripcion=None, request=None):
    """Función auxiliar para registrar una acción en el historial"""
    if not inmueble or not usuario:
        return
    
    ip_address = None
    user_agent = None
    
    if request:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
    
    HistorialUsoInmueble.objects.create(
        inmueble=inmueble,
        usuario=usuario,
        accion=accion,
        descripcion=descripcion,
        ip_address=ip_address,
        user_agent=user_agent
    )


@receiver(post_save, sender=Archivo)
def registrar_archivo_subido(sender, instance, created, **kwargs):
    """Registra cuando se sube un archivo"""
    if created and instance.inmueble:
        nombre_archivo = instance.archivo.name.split('/')[-1] if instance.archivo else 'sin nombre'
        registrar_accion(
            inmueble=instance.inmueble,
            usuario=instance.inmueble.assigned_to if hasattr(instance.inmueble, 'assigned_to') else None,
            accion='archivo_subido',
            descripcion=f"Archivo '{nombre_archivo}' subido"
        )


@receiver(post_save, sender=Observacion)
def registrar_observacion(sender, instance, created, **kwargs):
    """Registra cuando se agrega una observación"""
    if created and instance.task:
        registrar_accion(
            inmueble=instance.task,
            usuario=instance.usuario if hasattr(instance, 'usuario') else (instance.task.assigned_to if hasattr(instance.task, 'assigned_to') else None),
            accion='observacion_agregada',
            descripcion=f"Observación agregada: {instance.texto[:100] if instance.texto else 'Sin texto'}..."
        )


@receiver(post_save, sender=Comentario)
def registrar_comentario(sender, instance, created, **kwargs):
    """Registra cuando se agrega un comentario"""
    if created and hasattr(instance, 'observacion') and instance.observacion and instance.observacion.task:
        registrar_accion(
            inmueble=instance.observacion.task,
            usuario=instance.usuario if hasattr(instance, 'usuario') else (instance.observacion.task.assigned_to if hasattr(instance.observacion.task, 'assigned_to') else None),
            accion='comentario_agregado',
            descripcion=f"Comentario agregado: {instance.texto[:100] if instance.texto else 'Sin texto'}..."
        )


@receiver(post_save, sender=DictamenEstructuralIMP)
def registrar_dictamen(sender, instance, created, **kwargs):
    """Registra cuando se agrega un dictamen"""
    if created and instance.task:
        registrar_accion(
            inmueble=instance.task,
            usuario=instance.task.assigned_to if hasattr(instance.task, 'assigned_to') else None,
            accion='dictamen_agregado',
            descripcion=f"Dictamen estructural agregado"
        )


@receiver(post_save, sender=DocumentoPropiedadIMP)
def registrar_titulo(sender, instance, created, **kwargs):
    """Registra cuando se agrega un título de propiedad"""
    if created and instance.task:
        registrar_accion(
            inmueble=instance.task,
            usuario=instance.task.assigned_to if hasattr(instance.task, 'assigned_to') else None,
            accion='titulo_agregado',
            descripcion=f"Título de propiedad agregado"
        )


@receiver(post_save, sender=FoliosRealesIMP)
def registrar_folio(sender, instance, created, **kwargs):
    """Registra cuando se agrega un folio real"""
    if created and instance.task:
        registrar_accion(
            inmueble=instance.task,
            usuario=instance.task.assigned_to if hasattr(instance.task, 'assigned_to') else None,
            accion='folio_agregado',
            descripcion=f"Folio real agregado"
        )


@receiver(post_save, sender=Expedientes_CEDOCIMP)
def registrar_expediente(sender, instance, created, **kwargs):
    """Registra cuando se agrega un expediente CEDOC"""
    if created and instance.task:
        registrar_accion(
            inmueble=instance.task,
            usuario=instance.task.assigned_to if hasattr(instance.task, 'assigned_to') else None,
            accion='expediente_agregado',
            descripcion=f"Expediente CEDOC agregado"
        )


@receiver(pre_save, sender=Inmueble)
def registrar_cambios_inmueble(sender, instance, **kwargs):
    """Registra cambios en el estado o asignación del inmueble"""
    if instance.pk:  # Solo para actualizaciones, no para creación
        try:
            old_instance = Inmueble.objects.get(pk=instance.pk)
            
            # Verificar cambio de estado
            if old_instance.estado != instance.estado:
                registrar_accion(
                    inmueble=instance,
                    usuario=instance.assigned_to if hasattr(instance, 'assigned_to') else None,
                    accion='estado_cambiado',
                    descripcion=f"Estado cambiado de '{old_instance.estado}' a '{instance.estado}'"
                )
            
            # Verificar cambio de asignación
            if hasattr(old_instance, 'assigned_to') and hasattr(instance, 'assigned_to'):
                if old_instance.assigned_to != instance.assigned_to:
                    old_user = old_instance.assigned_to.username if old_instance.assigned_to else 'Sin asignar'
                    new_user = instance.assigned_to.username if instance.assigned_to else 'Sin asignar'
                    registrar_accion(
                        inmueble=instance,
                        usuario=instance.assigned_to,
                        accion='asignacion_cambiada',
                        descripcion=f"Asignación cambiada de '{old_user}' a '{new_user}'"
                    )
        except Inmueble.DoesNotExist:
            pass

