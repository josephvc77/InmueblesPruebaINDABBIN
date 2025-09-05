from django import forms
from django.forms import ClearableFileInput, ModelForm


from MDSJSEP.models import Task_eventos
from condia.models import TareasCondia
from .models import ColindanciasIMP, DatosAvaluosIMP, DatosLlamadasInmuebles, DatosTercerosIMP, DictamenEstructuralIMP, Documento_ocupacionIMP, DocumentoPropiedadIMP, EdificacionIMP, EdificioVerdeIMP, Expedientes_CEDOCIMP, FoliosRealesIMP, Inmueble, InstitucionesOcupantesIMP, MensajeIMP, NumeroPlanoIMP, Observaciones, OcupacionesIMP, RegistroLlamadas, TramitesDisposicionIMP
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from django import forms
from .models import CustomUser

# Formulario para crear o editar usuarios
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'puesto', 'is_active', 'is_staff', 'groups']

# Formulario para editar usuarios existentes
class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),  # Aquí usamos el queryset para los grupos
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Grupos",
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'groups']


# Formulario para crear un nuevo usuario
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrega la clase 'form-control' a todos los widgets del formulario
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})




class DatePickerWidget(forms.DateInput):
    input_type = 'date'

class CustomClearableFileInput(ClearableFileInput):
     template_with_clear='<br><label target="_blank" for="%(clear_checkbox_id)s formFile">%(clear_checkbox_label)s</label> %(clear)s'

class TaskCreateForm(ModelForm):
    class Meta:
        model = Inmueble
        fields = [
            'NombreInmueble', 
            'assigned_to', 
            'causa_alta', 
            'prioridad', 
            'deadline', 
            'creado', 
            'Sector', 
            'Nombre_de_la_institucion_que_administra_el_inmueble'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()

        # Flag para template
        self.assigned_to_visible = True
        if not user or not user.is_superuser:
            self.fields['assigned_to'].widget = forms.HiddenInput()
            self.assigned_to_visible = False

            
class MensajeFormIMP(forms.ModelForm):
    enviar_a_imp = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        label='Enviar A',
        required=False,  # <- Esto permite que no sea obligatorio
        widget=forms.Select(attrs={'class': 'form-control shadow-sm'})
    )

    class Meta:
        model = MensajeIMP
        fields = ['asunto', 'mensaje', 'enviar_a_imp', 'estado', 'enlace']

    

class PasswordConfirmationForm(forms.Form):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class SignInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    

class BajaForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['estado']
        
class SiteSelectionForm(forms.Form):
    SITIO_CHOICES = [
        ('microsite1', 'INDABBIN'),
        ('microsite2', 'CONDIA'),
        # Agrega más opciones de sitio según sea necesario
    ]

    site = forms.ChoiceField(
        label='Selecciona un sitio:',
        choices=SITIO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
    )
    
        
        
from django import forms
from .models import Inmueble

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = [
                # Encabezado - Datos generales
                  'rfi', 'assigned_to', 'deadline', 'rfiProv', 'NombreInmueble', 'UR', 'seccion_del_inventario', 'causa_alta', 'prioridad', 'Sector', 'Nombre_de_la_institucion_que_administra_el_inmueble', 'Naturaleza_Juridica_de_la_Institucion', 
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
                  'valor_construccion', 'valor_catastral_terreno', 'valor_catastral_construccion', 'valor_total_catastral', 'fecha_valor_catastral', 'documentacion_soporte', 'estado', 'important'
                  ]
        
        widgets = {
            # Datos generales
            'rfi': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rfiProv': forms.Select(attrs={'class': 'form-select'}),
            'NombreInmueble': forms.TextInput(attrs={'class': 'form-control'}),
            'UR': forms.Select(attrs={'class': 'form-select'}),
            'seccion_del_inventario': forms.TextInput(attrs={'class': 'form-control'}),
            'causa_alta': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'Sector': forms.Select(attrs={'class': 'form-select'}),
            'Nombre_de_la_institucion_que_administra_el_inmueble': forms.Select(attrs={'class': 'form-select'}),
            'Naturaleza_Juridica_de_la_Institucion': forms.Select(attrs={'class': 'form-select'}),
            'Denominaciones_anteriores': forms.TextInput(attrs={'class': 'form-control'}),
            'Dependencia_Administradora': forms.TextInput(attrs={'class': 'form-control'}),
            'subSeccion': forms.TextInput(attrs={'class': 'form-control'}),
            'certificado_de_seguridad': forms.Select(attrs={'class': 'form-select'}),
            'sentido_del_Dictamen': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_del_sentido_del_Dictamen': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_documento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'subir_archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'no_de_identificador_del_expediente_institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Ubicación
            'pais': forms.Select(attrs={'class': 'form-select'}),
            'entidad_federativa': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio_alcaldia': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio_no_existente': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'componente_espacial': forms.Select(attrs={'class': 'form-select'}),
            'fotografia_de_la_ubicacion': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tipo_vialidad': forms.Select(attrs={'class': 'form-select'}),
            'nombre_vialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_exterior': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_exterior_2': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_interior': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_asentamiento': forms.Select(attrs={'class': 'form-select'}),
            'nombre_asentamiento': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'entre_vialidades_referencia1': forms.TextInput(attrs={'class': 'form-control'}),
            'entre_vialidades_referencia2': forms.TextInput(attrs={'class': 'form-control'}),
            'vialidad_posterior': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_ubicacion': forms.Textarea(attrs={'class': 'form-control'}),
            'datum': forms.Select(attrs={'class': 'form-select'}),
            'utmx': forms.TextInput(attrs={'class': 'form-control'}),
            'utmy': forms.TextInput(attrs={'class': 'form-control'}),
            'utm_zona': forms.TextInput(attrs={'class': 'form-control'}),
            'latitud': forms.TextInput(attrs={'class': 'form-control'}),
            'longitud': forms.TextInput(attrs={'class': 'form-control'}),

            # Caracteristicas
            'superficie_del_terreno_en_M2': forms.TextInput(attrs={'class': 'form-control'}),
            'superficie_del_terreno_HA': forms.TextInput(attrs={'class': 'form-control'}),
            'superficie_de_desplante_en_M2': forms.TextInput(attrs={'class': 'form-control'}),
            'superficie_construida_en_M2': forms.TextInput(attrs={'class': 'form-control'}),
            'superficie_util_m2': forms.TextInput(attrs={'class': 'form-control'}),
            'zona_ubicacion': forms.Select(attrs={'class': 'form-select'}),
            'calidad_construccion': forms.Select(attrs={'class': 'form-select'}),
            'servicios': forms.Select(attrs={'class': 'form-select'}),
            'telefono_inmueble': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio_construccion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'siglo_construccion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ultima_remodelacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monumento': forms.Select(attrs={'class': 'form-select'}),
            'historico': forms.Select(attrs={'class': 'form-select'}),
            'artistico': forms.Select(attrs={'class': 'form-select'}),
            'arqueologico': forms.Select(attrs={'class': 'form-select'}),
            'clave_inah': forms.TextInput(attrs={'class': 'form-control'}),
            'folio_real_inah': forms.TextInput(attrs={'class': 'form-control'}),
            'no_plano_inah': forms.TextInput(attrs={'class': 'form-control'}),
            'clave_cnmh': forms.TextInput(attrs={'class': 'form-control'}),
            'clave_dgsmpc_conaculta': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inscripcion_unesco': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones_historicas': forms.Textarea(attrs={'class': 'form-control'}),
            'siglo_o_periodo': forms.TextInput(attrs={'class': 'form-control'}),
            'correlativo': forms.TextInput(attrs={'class': 'form-control'}),
            'conjunto': forms.TextInput(attrs={'class': 'form-control'}),
            'clave_inbal': forms.TextInput(attrs={'class': 'form-control'}),
            'registro_unico_inah': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_conservacion': forms.Select(attrs={'class': 'form-select'}),
            'tipo_inmueble_rural': forms.Select(attrs={'class': 'form-select'}),
            'uso_dominante_zona': forms.Select(attrs={'class': 'form-select'}),
            'clasificacion_edad': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'grado_consolidacion': forms.Select(attrs={'class': 'form-select'}),

            # Uso
            'usuario_principal_del_inmueble': forms.TextInput(attrs={'class': 'form-control'}),
            'usoGenerico': forms.TextInput(attrs={'class': 'form-control'}),
            'usoEspecifico': forms.TextInput(attrs={'class': 'form-control'}),
            'uso_de_suelo_autorizado': forms.Select(attrs={'class': 'form-select'}),
            'numero_de_empleados_en_el_inmueble': forms.TextInput(attrs={'class': 'form-control'}),
            'documento_que_autoriza_ocupacion': forms.Select(attrs={'class': 'form-select'}),
            'numero_de_documentos_de_ocupacion': forms.TextInput(attrs={'class': 'form-control'}),
            'instituciones_ocupantes': forms.Select(attrs={'class': 'form-select'}),
            'usuarios_terceros': forms.Select(attrs={'class': 'form-select'}),

            # Aprovechamiento
            'aprovechamiento': forms.Select(attrs={'class': 'form-select'}),
            'inmueble_con_atencion_al_publico': forms.Select(attrs={'class': 'form-select'}),
            'poblacion_beneficiada': forms.TextInput(attrs={'class': 'form-control'}),
            'poblacion_servicio': forms.Textarea(attrs={'class': 'form-control'}),
            'cuenta_con_proyecto_de_uso_inmediato_desarrollado': forms.Select(attrs={'class': 'form-select'}),
            'inversion_requerida': forms.TextInput(attrs={'class': 'form-control'}),
            'fuente_financiamiento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_solicitud': forms.TextInput(attrs={'class': 'form-control'}),
            'inmueble_no_aprovechable_especificar': forms.Textarea(attrs={'class': 'form-control'}),
            'gasto_anual_de_mantenimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'inmueble_en_condominio': forms.Select(attrs={'class': 'form-select'}),
            'superficie_total': forms.TextInput(attrs={'class': 'form-control'}),
            'indiviso': forms.TextInput(attrs={'class': 'form-control'}),

            # Valor
            'valor_contable': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_valor_contable': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_asegurable': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_valor_asegurable': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_adquisicion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_valor_adquisicion': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_terreno': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_construccion': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_catastral_terreno': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_catastral_construccion': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_total_catastral': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_valor_catastral': forms.TextInput(attrs={'class': 'form-control'}),
            'documentacion_soporte': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class DictamenEstructuralIMPForm(forms.ModelForm):
    class Meta:
        model = DictamenEstructuralIMP
        fields = [
            'no_de_identificador_del_expediente_institucion', 'subir_archivo_dictamen', 
            'certificado_de_seguridad', 'sentido_del_Dictamen', 'descripcion_del_sentido_del_Dictamen',
            'fecha_documento',
        ]
        widgets = {
            'no_de_identificador_del_expediente_institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'subir_archivo_dictamen': CustomClearableFileInput(attrs={'class': 'form-control'}),
            'certificado_de_seguridad': forms.TextInput(attrs={'class': 'form-control'}),
            'sentido_del_Dictamen': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_del_sentido_del_Dictamen': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_documento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ObservacionesForm(forms.ModelForm):
    class Meta:
        model = Observaciones
        fields = ['observaciones_data', 'fecha_observacion']
        widgets = {
            'observaciones_data': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_observacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class FoliosRealesIMPForm(forms.ModelForm):
    class Meta:
        model = FoliosRealesIMP
        fields = ['folios_reales_data', 'archivo_folios_reales']
        widgets = {
            'folios_reales_data': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo_folios_reales': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class NumeroPlanoIMPForm(forms.ModelForm):
    class Meta:
        model = NumeroPlanoIMP
        fields = ['numero_plano_data', 'archivo_Numero_Plano']
        widgets = {
            'numero_plano_data': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo_Numero_Plano': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class Expedientes_CEDOCIMPForm(forms.ModelForm):
    class Meta:
        model = Expedientes_CEDOCIMP
        fields = ['expediente_cedoc_data', 'archivo_Expedientes_CEDOC']
        widgets = {
            'expediente_cedoc_data': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo_Expedientes_CEDOC': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class DocumentoPropiedadIMPForm(forms.ModelForm):
    class Meta:
        model = DocumentoPropiedadIMP
        fields = [
            'fecha_creacion_DOC', 'archivo', 'propietario_inmueble', 
            'institucion_propietario', 'superficie_amparada_m2', 'tipo_documento', 
            'numero_de_documento', 'expedido_por', 'inscripcion_rppf', 
            'folio_real_federal', 'fecha_inscripcion_federal', 'inscripcion_registro_local', 
            'folio_real_local', 'folio_real_auxiliar', 'nombre_libro', 'tomo_o_volumen', 
            'numero', 'foja_o_folio', 'seccion', 'fecha_inscripcion_local',
        ]
        widgets = {
            'fecha_creacion_DOC': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'archivo': CustomClearableFileInput(attrs={'class': 'form-control'}),
            'propietario_inmueble': forms.Select(attrs={'class': 'form-select'}),
            'institucion_propietario': forms.TextInput(attrs={'class': 'form-control'}),
            'superficie_amparada_m2': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'numero_de_documento': forms.NumberInput(attrs={'class': 'form-control'}),
            'expedido_por': forms.TextInput(attrs={'class': 'form-control'}),
            'inscripcion_rppf': forms.Select(attrs={'class': 'form-select'}),
            'folio_real_federal': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inscripcion_federal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'inscripcion_registro_local': forms.Select(attrs={'class': 'form-select'}),
            'folio_real_local': forms.TextInput(attrs={'class': 'form-control'}),
            'folio_real_auxiliar': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_libro': forms.TextInput(attrs={'class': 'form-control'}),
            'tomo_o_volumen': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'foja_o_folio': forms.TextInput(attrs={'class': 'form-control'}),
            'seccion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inscripcion_local': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
# CONDIA ---------------------------------------------------------------------

class CondiaForm(forms.ModelForm):
    class Meta:
        model = TareasCondia
        fields = [
            'titulo', 'descripcion','uso_inmueble','riuf','superficie_rentable',
            'superficie_terreno','superficie_construida','personal_ocupante','uso_suelo','renta_mensual_civa_segun_contrato', 'monto_por_m2_civa','ubicacion',
            'no_contrato','fecha_firma_contrato','monto_mensual_dictamen_estructural', 'tipo_de_proceso',
            'correo1','correo2','razon_social','propietario_representante','identificacion_oficial',
            'email','domicilio_fiscal','justificacion_de_renta','nombre_asentamiento', 'codigo_postal','descripcion_ubicacion', 'fotoPresentacion', 
            # Archivos
            
            'solicitud_espacio', 'tabla_superficie_maxima', 'justificacion_arrendamiento', 'solicitud_disponibilidad', 'solicitud_arrendamiento_oficialia', 'notificacion_propietario_arrendar',
            'solicitud_justipreciacion_renta', 'notificacion_pago_derechos', 'dictamen_justipreciacion_renta', 'oficio_revision_juridica_respuesta', 'justificacion_plurianual', 'oficio_solicitud_registro_obligacional',
            'registro_contrato_pagina_indaabin', 'contrato_arrendamiento_convenios', 'notificacion_ur_subdireccion_obras_planos', 'anexo_contrato_acta_recepcion_inmueble', 'documentos_inventario_condiciones',
            'documentos_dictamen_seguridad_estructural', 'documentos_usos_limitaciones', 'documentos_acta_entrega_trabajos', 'anexo_contrato_plano_distribucion_personal', 'notificacion_disponibilidad_ur',
            'actas_entrega_asignacion_espacio', 'documentos_legales_escritura_inmueble', 'documentos_legales_acta_constitutiva', 'documentos_legales_escritura_cambio_regimen', 'documentos_legales_poder_notarial',
            'documentos_legales_cedula_fiscal', 'documentos_legales_identificacion_oficial', 'documentos_legales_comprobante_domicilio_fiscal', 'documentos_tecnicos_planos_arquitectonicos', 
            'documentos_tecnicos_constancia_seguridad_estructural', 'documentos_tecnicos_visto_bueno_seguridad_operacion', 'documentos_tecnicos_ultimo_pago_predial', 'documentos_tecnicos_ultimo_pago_agua',
            'documentos_tecnicos_ultimo_pago_energia', 'fundamento_legal'
        ]
        widgets = {
            'renta_mensual_civa_segun_contrato': forms.TextInput(attrs={'class': 'bg', 'placeholder': 'Ingresa un Monto', 'id': 'renta_mensual_civa_segun_contrato'}),
            'monto_por_m2_civa': forms.TextInput(attrs={'class': 'bg', 'placeholder': 'Ingresa un Monto',}),
            'ubicacion': forms.TextInput(attrs={'class': 'bg', 'placeholder': 'Ingresa la Ubicación',}),
        }

class CreateTaskCondiaForm(forms.ModelForm):
    class Meta:
        model = TareasCondia
        fields = [
            'titulo', 'descripcion'
        ]


# SALAS DE JUNTAS
class CreateTaskSalasForm(forms.ModelForm):
    class Meta:
        model = Task_eventos
        fields = [
            'titulo', 'descripcion'
        ]

class SalasForm(forms.ModelForm):
    class Meta:
        model = Task_eventos
        fields = [
            'titulo', 'descripcion'
        ]



class CreateDatosLlamadasForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=False, label='Assigned to')

    class Meta:
        model = DatosLlamadasInmuebles
        fields = ['NombreInmueble', 'deadline', 'prioridad', 'assigned_task', 'nombre_del_contacto', 'puesto_o_cargo', 'tel_plantel', 'estatus_llamada', 'ur']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateDatosLlamadasForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['assigned_task'].queryset = CustomUser.objects.filter(username=user.username)
            
             # Agregar clases CSS a todos los campos automáticamente
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()


from django import forms
from .models import DatosLlamadasInmuebles
from django.contrib.auth import get_user_model

User = get_user_model()

class DatosLlamadasInmueblesForm(forms.ModelForm):
    class Meta:
        model = DatosLlamadasInmuebles
        fields = [
            'NombreInmueble', 'rfi', 'estado', 'deadline', 'prioridad', 'assigned_task',
            'edo', 'nd', 'nombre_del_contacto', 'puesto_o_cargo', 'tel_plantel',
            'ext', 'celular', 'email', 'estatus_llamada', 'ur', 'observaciones'
        ]
        widgets = {
            'NombreInmueble': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del inmueble'}),
            'rfi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RFI'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'assigned_task': forms.Select(attrs={'class': 'form-select'}),
            'edo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
            'nd': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ND'}),
            'nombre_del_contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del contacto'}),
            'puesto_o_cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Puesto o cargo'}),
            'tel_plantel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono del plantel'}),
            'ext': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Extensión'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'estatus_llamada': forms.Select(attrs={'class': 'form-select'}),
            'ur': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos obligatorios
        self.fields['NombreInmueble'].required = True
        self.fields['estado'].required = True


# forms.py
from django import forms
from .models import RegistroLlamadas

class RegistroLlamadasForm(forms.ModelForm):
    class Meta:
        model = RegistroLlamadas
        fields = [
            "NumLlamada",
            "fecha_llamada",
            "hora_llamada",
            "acuerdos_compromisos",
            "fecha_comprometida",
            "fecha_respuesta_email",
            "fecha_revision_correcciones",
            "fecha_envio_correccion",
            "fecha_aprobacion_fichas_corregidas",
            "observaciones_generales",
            "fecha_compromiso_de_envio_de_informacion",
            "fecha_compromiso_de_observaciones_subsanadas",
            "fecha_autorizacion_de_documento",
            "finalizacion",
        ]
        widgets = {
            "fecha_llamada": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "hora_llamada": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "fecha_comprometida": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_respuesta_email": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_revision_correcciones": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_envio_correccion": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_aprobacion_fichas_corregidas": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_compromiso_de_envio_de_informacion": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_compromiso_de_observaciones_subsanadas": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_autorizacion_de_documento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "finalizacion": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "NumLlamada": forms.TextInput(attrs={"class": "form-control"}),
            "acuerdos_compromisos": forms.TextInput(attrs={"class": "form-control"}),
            "observaciones_generales": forms.TextInput(attrs={"class": "form-control"}),
        }

