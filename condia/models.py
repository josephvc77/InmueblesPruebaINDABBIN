from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from tasks.models import CustomUser
import os
import uuid

def get_upload_path(folder_name, field_name):
    """Genera una función de upload_path organizada por inmueble y carpeta"""
    def upload_path(instance, filename):
        # Obtener el ID del inmueble
        inmueble_id = instance.id if instance.id else 'temp'
        
        # Limpiar el nombre del archivo
        name, ext = os.path.splitext(filename)
        name_clean = slugify(name)
        filename_clean = f"{name_clean}_{uuid.uuid4().hex[:8]}{ext}"
        
        # Crear ruta organizada: condia/inmuebles/{id}/{carpeta}/{nombre_campo}/{archivo}
        return f'condia/inmuebles/{inmueble_id}/{folder_name}/{slugify(field_name)}/{filename_clean}'
    
    return upload_path

class InmuebleCondia(models.Model):
    NombreInmueble = models.CharField(max_length=150, verbose_name='Nombre del inmueble', null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    creado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Quien lo creó', related_name='inmuebles_condia_creados')
    
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Baja', 'Baja'),
        ('Completado', 'Completado'),
    ]
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Activo', null=True, blank=True)
    
    prioridad = models.CharField(
        max_length=10, 
        choices=[('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja')], 
        default='Media', 
        null=True, 
        blank=True
    )
    
    actualizado = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    # Carpeta 1: Procesos de Arrendamiento
    solicitud_espacio_ur = models.FileField(upload_to='condia/inmuebles/solicitud_espacio_ur/', null=True, blank=True)
    tabla_superficie_maxima = models.FileField(upload_to='condia/inmuebles/tabla_superficie_maxima/', null=True, blank=True)
    justificacion_autorizacion_indabin = models.FileField(upload_to='condia/inmuebles/justificacion_autorizacion_indabin/', null=True, blank=True)
    solicitud_disponibilidad_inmuebles = models.FileField(upload_to='condia/inmuebles/solicitud_disponibilidad_inmuebles/', null=True, blank=True)
    solicitud_autorizacion_oficialia_mayor = models.FileField(upload_to='condia/inmuebles/solicitud_autorizacion_oficialia_mayor/', null=True, blank=True)
    notificacion_al_propietario_para_arrendar_el_inmueble = models.FileField(upload_to='condia/inmuebles/notificacion_al_propietario_para_arrendar_el_inmueble/', null=True, blank=True)
    solicitud_de_justipreciacion_de_renta = models.FileField(upload_to='condia/inmuebles/solicitud_de_justipreciacion_de_renta/', null=True, blank=True)
    notificacion_de_pago_de_derechos_del_indabin = models.FileField(upload_to='condia/inmuebles/notificacion_de_pago_de_derechos_del_indabin/', null=True, blank=True)
    dictamen_de_justipreciacion_de_renta = models.FileField(upload_to='condia/inmuebles/dictamen_de_justipreciacion_de_renta/', null=True, blank=True)
    oficio_de_revision_juridica_y_respuesta = models.FileField(upload_to='condia/inmuebles/oficio_de_revision_juridica_y_respuesta/', null=True, blank=True)
    justificacion_plurianual = models.FileField(upload_to='condia/inmuebles/justificacion_plurianual/', null=True, blank=True)
    oficio_de_solicitud_y_registro_obligacional_uaj = models.FileField(upload_to='condia/inmuebles/oficio_de_solicitud_y_registro_obligacional_uaj/', null=True, blank=True)
    registro_de_contrato_en_pagina_del_indabin = models.FileField(upload_to='condia/inmuebles/registro_de_contrato_en_pagina_del_indabin/', null=True, blank=True)
    contrato_de_arrendamiento_y_convenios = models.FileField(upload_to='condia/inmuebles/contrato_de_arrendamiento_y_convenios/', null=True, blank=True)
    notificacion_a_la_ur_y_subdireccion_de_obras_para_la_elaboracion_de_los_planos_de_adecuacion_de_oficinas = models.FileField(upload_to='condia/inmuebles/notificacion_a_la_ur_y_subdireccion_de_obras_para_la_elaboracion_de_los_planos_de_adecuacion_de_oficinas/', null=True, blank=True, db_column='notif_ur_subdir_obras_planos_adecuacion')
    anexo_1_al_contrato_de_arrendamiento_acta_recepcion_del_inmueble = models.FileField(upload_to='condia/inmuebles/anexo_1_al_contrato_de_arrendamiento_acta_recepcion_del_inmueble/', null=True, blank=True)
    inventario_y_las_condiciones_de_instalaciones_y_equipos_propios_del_inmueble_validado_por_la_subdireccion_de_obras = models.FileField(upload_to='condia/inmuebles/inventario_y_las_condiciones_de_instalaciones_y_equipos_propios_del_inmueble_validado_por_la_subdireccion_de_obras/', null=True, blank=True, db_column='inventario_condiciones_instalaciones_equipos')
    dictamen_de_seguridad_estructural_emitido_por_un_director_responsable_del_inmueble = models.FileField(upload_to='condia/inmuebles/dictamen_de_seguridad_estructural_emitido_por_un_director_responsable_del_inmueble/', null=True, blank=True, db_column='dictamen_seguridad_estructural_director')
    usos_permitidos_y_en_general_todas_las_limitaciones_derivadas_de_las_caracteristicas_del_inmueble = models.FileField(upload_to='condia/inmuebles/usos_permitidos_y_en_general_todas_las_limitaciones_derivadas_de_las_caracteristicas_del_inmueble/', null=True, blank=True, db_column='usos_permitidos_limitaciones_inmueble')
    acta_entrega_de_los_trabajos_de_adecuacion_de_oficinas_a_cargo_de_la_subdireccion_de_obras = models.FileField(upload_to='condia/inmuebles/acta_entrega_de_los_trabajos_de_adecuacion_de_oficinas_a_cargo_de_la_subdireccion_de_obras/', null=True, blank=True, db_column='acta_entrega_trabajos_adecuacion_oficinas')
    anexo_2_al_contrato_de_arrendamiento_plano_de_distribucion_de_personal_adecuacion_de_oficinas_autorizado = models.FileField(upload_to='condia/inmuebles/anexo_2_al_contrato_de_arrendamiento_plano_de_distribucion_de_personal_adecuacion_de_oficinas_autorizado/', null=True, blank=True, db_column='anexo_2_contrato_plano_distribucion_personal')
    oficio_de_notificacion_de_disponibilidad_del_inmueble_a_la_ur = models.FileField(upload_to='condia/inmuebles/oficio_de_notificacion_de_disponibilidad_del_inmueble_a_la_ur/', null=True, blank=True)
    actas_entrega_de_asignacion_de_espacio_a_las_unidades_administrativas = models.FileField(upload_to='condia/inmuebles/actas_entrega_de_asignacion_de_espacio_a_las_unidades_administrativas/', null=True, blank=True, db_column='actas_entrega_asignacion_espacio_ur')

 
    # Carpeta 2: Documentación Legal y técnica
    documentacion_legal = models.FileField(upload_to='condia/inmuebles/documentacion_legal/', null=True, blank=True)
    escritura_inmueble_arrendar = models.FileField(upload_to='condia/inmuebles/escritura_inmueble_arrendar/', null=True, blank=True)
    testimonio_escritura_publica = models.FileField(upload_to='condia/inmuebles/testimonio_escritura_publica/', null=True, blank=True)
    escritura_de_cambio_de_regimen = models.FileField(upload_to='condia/inmuebles/escritura_de_cambio_de_regimen/', null=True, blank=True)
    escritura_publica_que_contenga_el_poder_notarial = models.FileField(upload_to='condia/inmuebles/escritura_publica_que_contenga_el_poder_notarial/', null=True, blank=True)
    cedula_de_identificacion_fiscal_del_arrendador = models.FileField(upload_to='condia/inmuebles/cedula_de_identificacion_fiscal_del_arrendador/', null=True, blank=True)
    identificacion_oficial_vigente_con_fotografia_y_firma_del_arrendador_o_representante_legal = models.FileField(upload_to='condia/inmuebles/identificacion_oficial_vigente_con_fotografia_y_firma_del_arrendador_o_representante_legal/', null=True, blank=True, db_column='identificacion_oficial_arrendador_rep_legal')
    comprobante_de_domicilio_fiscal_del_arrendador = models.FileField(upload_to='condia/inmuebles/comprobante_de_domicilio_fiscal_del_arrendador/', null=True, blank=True)
    documentacion_tecnica = models.FileField(upload_to='condia/inmuebles/documentacion_tecnica/', null=True, blank=True)
    planos_arquitectonicos = models.FileField(upload_to='condia/inmuebles/planos_arquitectonicos/', null=True, blank=True)
    registro_de_la_constancia_de_seguridad_estructural_expedida_por_el_gcdmx = models.FileField(upload_to='condia/inmuebles/registro_de_la_constancia_de_seguridad_estructural_expedida_por_el_gcdmx/', null=True, blank=True, db_column='registro_constancia_seguridad_estructural_gcdmx')
    visto_bueno_de_seguridad_y_operacion_expedida_por_el_gcdmx = models.FileField(upload_to='condia/inmuebles/visto_bueno_de_seguridad_y_operacion_expedida_por_el_gcdmx/', null=True, blank=True)
    ultima_boleta_por_concepto_de_pago_del_inmueble_predial = models.FileField(upload_to='condia/inmuebles/ultima_boleta_por_concepto_de_pago_del_inmueble_predial/', null=True, blank=True)
    ultima_boleta_por_concepto_de_suministro_de_agua_potable = models.FileField(upload_to='condia/inmuebles/ultima_boleta_por_concepto_de_suministro_de_agua_potable/', null=True, blank=True)
    ultimo_recibo_por_concepto_de_pago_de_servicio_de_energia_electrica = models.FileField(upload_to='condia/inmuebles/ultimo_recibo_por_concepto_de_pago_de_servicio_de_energia_electrica/', null=True, blank=True, db_column='ultimo_recibo_pago_servicio_energia_electrica')
    
    # Carpeta 3: Fundamento Legal
    fundamento_legal = models.FileField(upload_to='condia/inmuebles/fundamento_legal/', null=True, blank=True)
  
    

