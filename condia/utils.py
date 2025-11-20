"""
Utilidades para CONDIA - Gestión de archivos y estadísticas
"""

def get_file_fields_by_folder():
    """
    Retorna un diccionario con los campos de archivo organizados por carpeta.
    Incluye metadata para cada campo.
    """
    return {
        'carpeta_1': {
            'nombre': 'Procesos de Arrendamiento',
            'icono': 'bi-folder2-open',
            'color': '#611232',
            'campos': [
                {
                    'field': 'solicitud_espacio_ur',
                    'label': 'Solicitud de espacio o notificación a la UR',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'tabla_superficie_maxima',
                    'label': 'Tabla de superficie máxima',
                    'icono': 'bi-file-earmark-excel',
                },
                {
                    'field': 'justificacion_autorizacion_indabin',
                    'label': 'Justificación y autorización (INDAABIN)',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'solicitud_disponibilidad_inmuebles',
                    'label': 'Solicitud disponibilidad de inmuebles',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'solicitud_autorizacion_oficialia_mayor',
                    'label': 'Autorización Oficialía Mayor',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'notificacion_al_propietario_para_arrendar_el_inmueble',
                    'label': 'Notificación al propietario para arrendar',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'solicitud_de_justipreciacion_de_renta',
                    'label': 'Solicitud de justipreciación de renta',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'notificacion_de_pago_de_derechos_del_indabin',
                    'label': 'Notificación de pago de derechos INDAABIN',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'dictamen_de_justipreciacion_de_renta',
                    'label': 'Dictamen de justipreciación de renta',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'oficio_de_revision_juridica_y_respuesta',
                    'label': 'Oficio de revisión jurídica y respuesta',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'justificacion_plurianual',
                    'label': 'Justificación plurianual',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'oficio_de_solicitud_y_registro_obligacional_uaj',
                    'label': 'Oficio solicitud y registro obligacional UAJ',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'registro_de_contrato_en_pagina_del_indabin',
                    'label': 'Registro de contrato en página INDAABIN',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'contrato_de_arrendamiento_y_convenios',
                    'label': 'Contrato de arrendamiento y convenios',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'notificacion_a_la_ur_y_subdireccion_de_obras_para_la_elaboracion_de_los_planos_de_adecuacion_de_oficinas',
                    'label': 'Notificación a UR/Obras para planos de adecuación',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'anexo_1_al_contrato_de_arrendamiento_acta_recepcion_del_inmueble',
                    'label': 'Anexo 1 - Acta recepción del inmueble',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'inventario_y_las_condiciones_de_instalaciones_y_equipos_propios_del_inmueble_validado_por_la_subdireccion_de_obras',
                    'label': 'Inventario y condiciones (validado Obras)',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'dictamen_de_seguridad_estructural_emitido_por_un_director_responsable_del_inmueble',
                    'label': 'Dictamen de seguridad estructural',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'usos_permitidos_y_en_general_todas_las_limitaciones_derivadas_de_las_caracteristicas_del_inmueble',
                    'label': 'Usos permitidos y limitaciones',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'acta_entrega_de_los_trabajos_de_adecuacion_de_oficinas_a_cargo_de_la_subdireccion_de_obras',
                    'label': 'Acta entrega trabajos adecuación',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'anexo_2_al_contrato_de_arrendamiento_plano_de_distribucion_de_personal_adecuacion_de_oficinas_autorizado',
                    'label': 'Anexo 2 - Plano distribución personal',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'oficio_de_notificacion_de_disponibilidad_del_inmueble_a_la_ur',
                    'label': 'Oficio notificación disponibilidad a UR',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'actas_entrega_de_asignacion_de_espacio_a_las_unidades_administrativas',
                    'label': 'Actas entrega asignación espacio',
                    'icono': 'bi-file-earmark-pdf',
                },
            ]
        },
        'carpeta_2': {
            'nombre': 'Documentación Legal y Técnica',
            'icono': 'bi-folder2-open',
            'color': '#8b1f43',
            'campos': [
                {
                    'field': 'documentacion_legal',
                    'label': 'Documentación legal general',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'escritura_inmueble_arrendar',
                    'label': 'Escritura del inmueble a arrendar',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'testimonio_escritura_publica',
                    'label': 'Testimonio de la escritura pública',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'escritura_de_cambio_de_regimen',
                    'label': 'Escritura de cambio de régimen',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'escritura_publica_que_contenga_el_poder_notarial',
                    'label': 'Escritura con poder notarial',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'cedula_de_identificacion_fiscal_del_arrendador',
                    'label': 'Cédula identificación fiscal arrendador',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'identificacion_oficial_vigente_con_fotografia_y_firma_del_arrendador_o_representante_legal',
                    'label': 'Identificación oficial vigente',
                    'icono': 'bi-file-earmark-image',
                },
                {
                    'field': 'comprobante_de_domicilio_fiscal_del_arrendador',
                    'label': 'Comprobante domicilio fiscal',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'documentacion_tecnica',
                    'label': 'Documentación técnica general',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'planos_arquitectonicos',
                    'label': 'Planos arquitectónicos',
                    'icono': 'bi-file-earmark-image',
                },
                {
                    'field': 'registro_de_la_constancia_de_seguridad_estructural_expedida_por_el_gcdmx',
                    'label': 'Constancia seguridad estructural (GCDMX)',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'visto_bueno_de_seguridad_y_operacion_expedida_por_el_gcdmx',
                    'label': 'Visto bueno seguridad y operación',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'ultima_boleta_por_concepto_de_pago_del_inmueble_predial',
                    'label': 'Última boleta predial',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'ultima_boleta_por_concepto_de_suministro_de_agua_potable',
                    'label': 'Última boleta agua potable',
                    'icono': 'bi-file-earmark-pdf',
                },
                {
                    'field': 'ultimo_recibo_por_concepto_de_pago_de_servicio_de_energia_electrica',
                    'label': 'Último recibo energía eléctrica',
                    'icono': 'bi-file-earmark-pdf',
                },
            ]
        },
        'carpeta_3': {
            'nombre': 'Fundamento Legal',
            'icono': 'bi-folder2-open',
            'color': '#A57F2C',
            'campos': [
                {
                    'field': 'fundamento_legal',
                    'label': 'Documento de Fundamento Legal',
                    'icono': 'bi-file-earmark-pdf',
                },
            ]
        },
    }


def get_document_statistics(inmueble):
    """
    Calcula estadísticas de documentos para un inmueble.
    Retorna un diccionario con información de cada carpeta.
    """
    folders_info = get_file_fields_by_folder()
    statistics = {}
    
    for folder_key, folder_data in folders_info.items():
        total = len(folder_data['campos'])
        uploaded = 0
        missing = []
        
        for campo_info in folder_data['campos']:
            field_name = campo_info['field']
            field_value = getattr(inmueble, field_name, None)
            
            if field_value:
                uploaded += 1
            else:
                missing.append(campo_info['label'])
        
        percentage = (uploaded / total * 100) if total > 0 else 0
        
        statistics[folder_key] = {
            'nombre': folder_data['nombre'],
            'icono': folder_data['icono'],
            'color': folder_data['color'],
            'total': total,
            'uploaded': uploaded,
            'missing': missing,
            'percentage': round(percentage, 1),
            'is_complete': uploaded == total,
        }
    
    # Estadísticas generales
    total_docs = sum(s['total'] for s in statistics.values())
    total_uploaded = sum(s['uploaded'] for s in statistics.values())
    overall_percentage = (total_uploaded / total_docs * 100) if total_docs > 0 else 0
    
    statistics['_general'] = {
        'total': total_docs,
        'uploaded': total_uploaded,
        'percentage': round(overall_percentage, 1),
    }
    
    return statistics


def get_file_extension_icon(filename):
    """Retorna el icono de Bootstrap Icons según la extensión del archivo"""
    if not filename:
        return 'bi-file-earmark'
    
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    icon_map = {
        'pdf': 'bi-file-earmark-pdf-fill',
        'doc': 'bi-file-earmark-word-fill',
        'docx': 'bi-file-earmark-word-fill',
        'xls': 'bi-file-earmark-excel-fill',
        'xlsx': 'bi-file-earmark-excel-fill',
        'jpg': 'bi-file-earmark-image-fill',
        'jpeg': 'bi-file-earmark-image-fill',
        'png': 'bi-file-earmark-image-fill',
        'gif': 'bi-file-earmark-image-fill',
        'zip': 'bi-file-earmark-zip-fill',
        'rar': 'bi-file-earmark-zip-fill',
    }
    
    return icon_map.get(ext, 'bi-file-earmark-fill')

