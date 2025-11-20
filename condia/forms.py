from django import forms
from .models import InmuebleCondia

class InmuebleCondiaForm(forms.ModelForm):
    """Formulario para creación básica o edición rápida"""
    class Meta:
        model = InmuebleCondia
        fields = ['NombreInmueble', 'descripcion', 'estado', 'prioridad']
        widgets = {
            'NombreInmueble': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del inmueble'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ingrese una descripción del inmueble'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'NombreInmueble': 'Nombre del inmueble',
            'descripcion': 'Descripción',
            'estado': 'Estado',
            'prioridad': 'Prioridad',
        }

class InmuebleCondiaEditarForm(forms.ModelForm):
    """
    Formulario completo para la vista de detalle.
    Incluye lógica automática para estilizar los inputs de archivos.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recorremos todos los campos para aplicar estilos, especialmente a los FileFields
        for field_name, field in self.fields.items():
            # Si es un campo de archivo
            if isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png'
                })
            # Si es otro tipo de campo, aseguramos estilo bootstrap básico
            elif 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = InmuebleCondia
        fields = [
            # Campos básicos
            'NombreInmueble', 
            'descripcion', 
            'estado', 
            'prioridad',
            
            # Carpeta 1: Procesos de Arrendamiento
            'solicitud_espacio_ur',
            'tabla_superficie_maxima',
            'justificacion_autorizacion_indabin',
            'solicitud_disponibilidad_inmuebles',
            'solicitud_autorizacion_oficialia_mayor',
            'notificacion_al_propietario_para_arrendar_el_inmueble',
            'solicitud_de_justipreciacion_de_renta',
            'notificacion_de_pago_de_derechos_del_indabin',
            'dictamen_de_justipreciacion_de_renta',
            'oficio_de_revision_juridica_y_respuesta',
            'justificacion_plurianual',
            'oficio_de_solicitud_y_registro_obligacional_uaj',
            'registro_de_contrato_en_pagina_del_indabin',
            'contrato_de_arrendamiento_y_convenios',
            'notificacion_a_la_ur_y_subdireccion_de_obras_para_la_elaboracion_de_los_planos_de_adecuacion_de_oficinas',
            'anexo_1_al_contrato_de_arrendamiento_acta_recepcion_del_inmueble',
            'inventario_y_las_condiciones_de_instalaciones_y_equipos_propios_del_inmueble_validado_por_la_subdireccion_de_obras',
            'dictamen_de_seguridad_estructural_emitido_por_un_director_responsable_del_inmueble',
            'usos_permitidos_y_en_general_todas_las_limitaciones_derivadas_de_las_caracteristicas_del_inmueble',
            'acta_entrega_de_los_trabajos_de_adecuacion_de_oficinas_a_cargo_de_la_subdireccion_de_obras',
            'anexo_2_al_contrato_de_arrendamiento_plano_de_distribucion_de_personal_adecuacion_de_oficinas_autorizado',
            'oficio_de_notificacion_de_disponibilidad_del_inmueble_a_la_ur',
            'actas_entrega_de_asignacion_de_espacio_a_las_unidades_administrativas',

            # Carpeta 2: Documentación Legal y técnica
            'documentacion_legal',
            'escritura_inmueble_arrendar',
            'testimonio_escritura_publica',
            'escritura_de_cambio_de_regimen',
            'escritura_publica_que_contenga_el_poder_notarial',
            'cedula_de_identificacion_fiscal_del_arrendador',
            'identificacion_oficial_vigente_con_fotografia_y_firma_del_arrendador_o_representante_legal',
            'comprobante_de_domicilio_fiscal_del_arrendador',
            'documentacion_tecnica',
            'planos_arquitectonicos',
            'registro_de_la_constancia_de_seguridad_estructural_expedida_por_el_gcdmx',
            'visto_bueno_de_seguridad_y_operacion_expedida_por_el_gcdmx',
            'ultima_boleta_por_concepto_de_pago_del_inmueble_predial',
            'ultima_boleta_por_concepto_de_suministro_de_agua_potable',
            'ultimo_recibo_por_concepto_de_pago_de_servicio_de_energia_electrica',

            # Carpeta 3: Fundamento Legal
            'fundamento_legal'
        ]
        
        widgets = {
            'NombreInmueble': forms.TextInput(attrs={
                'class': 'form-control modern-input',
                'placeholder': 'Ingrese el nombre del inmueble'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control modern-textarea',
                'rows': 4,
                'placeholder': 'Ingrese una descripción del inmueble'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select modern-select'
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select modern-select'
            }),
        }