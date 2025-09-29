from import_export import resources
from .models import DatosLlamadasInmuebles, Inmueble

class InmuebleResource(resources.ModelResource):
    class Meta:
        model = Inmueble
        import_id_fields = ('rfi',)   # campo único en tu modelo
        fields = ('rfi', 'assigned_to', 'deadline', 'rfiProv', 'NombreInmueble', 'UR', 'seccion_del_inventario', 'causa_alta', 'prioridad', 'Sector', 'Nombre_de_la_institucion_que_administra_el_inmueble', 'Naturaleza_Juridica_de_la_Institucion', 
                  'Denominaciones_anteriores', 'Dependencia_Administradora', 'subSeccion','certificado_de_seguridad', 'sentido_del_Dictamen', 
                  'descripcion_del_sentido_del_Dictamen','fecha_documento', 'subir_archivo','no_de_identificador_del_expediente_institucion', 
                # Ubicación
                  'pais', 'entidad_federativa', 'municipio_alcaldia', 'municipio_no_existente', 'localidad', 'componente_espacial','fotografia_de_la_ubicacion',
                  'tipo_vialidad', 'nombre_vialidad', 'numero_exterior', 'numero_exterior_2', 'numero_interior',
                  'tipo_asentamiento', 'nombre_asentamiento', 'codigo_postal', 'entre_vialidades_referencia1',
                  'entre_vialidades_referencia2', 'vialidad_posterior', 'descripcion_ubicacion', 'datum', 'utmx', 'utmy', 'utm_zona', 'latitud', 'longitud',  
                # Caracteristicas
                  'superficie_del_terreno_en_M2','superficie_del_terreno_HA','superficie_de_desplante_en_M2','superficie_construida_en_M2','superficie_util_m2', 
                  'zona_ubicacion', 'tipo_inmueble_rural', 'uso_dominante_zona', 'calidad_construccion', 'clasificacion_edad', 'categoria', 'grado_consolidacion',
                  'servicios', 'telefono_inmueble', 'fecha_inicio_construccion', 'siglo_construccion', 'fecha_ultima_remodelacion', 'monumento',
                  'historico', 'artistico', 'arqueologico', 'estado_conservacion', 'clave_inah', 'folio_real_inah', 'no_plano_inah', 'clave_cnmh', 'clave_dgsmpc_conaculta', 'fecha_inscripcion_unesco', 'observaciones_historicas', 
                  
                # Uso
                  'usuario_principal_del_inmueble', 'usoGenerico', 'usoEspecifico', 'uso_de_suelo_autorizado','numero_de_empleados_en_el_inmueble',
                  'documento_que_autoriza_ocupacion', 'numero_de_documentos_de_ocupacion', 'instituciones_ocupantes','usuarios_terceros',
                  'siglo_o_periodo', 'correlativo', 'conjunto', 'clave_inbal', 'registro_unico_inah', 
                # Aprovechamiento  
                  'aprovechamiento', 'inmueble_con_atencion_al_publico', 'poblacion_beneficiada', 'poblacion_servicio', 'cuenta_con_proyecto_de_uso_inmediato_desarrollado', 
                  'inversion_requerida', 'fuente_financiamiento', 'fecha_solicitud',
                  'inmueble_no_aprovechable_especificar', 'gasto_anual_de_mantenimiento',
                  'inmueble_en_condominio', 'superficie_total', 'indiviso',
            
                # Valor
                  'valor_contable', 'fecha_valor_contable', 'valor_asegurable', 'fecha_valor_asegurable', 'valor_adquisicion', 'fecha_valor_adquisicion', 'valor_terreno', 
                  'valor_construccion', 'valor_catastral_terreno', 'valor_catastral_construccion', 'valor_total_catastral', 'fecha_valor_catastral', 'documentacion_soporte', 'estado')
        skip_unchanged = True
        report_skipped = True



class LlamadaResource(resources.ModelResource):
    class Meta:
        model = DatosLlamadasInmuebles
        # Puedes especificar campos adicionales o personalizar la importación aquí