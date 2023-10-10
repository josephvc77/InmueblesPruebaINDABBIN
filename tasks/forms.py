from django import forms
from django.forms import ClearableFileInput, ModelForm
from .models import Colindancias, ColindanciasIMP, DatosAvaluos, DatosAvaluosIMP, DatosTerceros, DatosTercerosIMP, Documento_ocupacion, Documento_ocupacionIMP, DocumentoPropiedad, DocumentoPropiedadIMP, Edificacion, EdificacionIMP, EdificioVerde, EdificioVerdeIMP, Expedientes_CEDOC, Expedientes_CEDOCIMP, FoliosReales, FoliosRealesIMP, Inmueble, InstitucionesOcupantes, InstitucionesOcupantesIMP, Mensaje, NumeroPlano, NumeroPlanoIMP, Ocupaciones, OcupacionesIMP, Task, Task_Condia, TramitesDisposicion, TramitesDisposicionIMP

class DatePickerWidget(forms.DateInput):
    input_type = 'date'

class CustomClearableFileInput(ClearableFileInput):
     template_with_clear='<br><label target="_blank" for="%(clear_checkbox_id)s formFile">%(clear_checkbox_label)s</label> %(clear)s'

class FoliosRealesForm(forms.ModelForm):
    class Meta:
        model = FoliosReales
        fields = ['folios_reales_data']
        
class Numero_PlanoForm(forms.ModelForm):
    class Meta:
        model = NumeroPlano
        fields = ['numero_plano_data']
        
class Expedientes_CEDOCForm(forms.ModelForm):
    class Meta:
        model = Expedientes_CEDOC
        fields = ['expediente_cedoc_data']
        
class Edificio_VerdeForm(forms.ModelForm):
    class Meta:
        model = EdificioVerde
        fields = ['edificio_verde_data']

class EdificacionForm(forms.ModelForm):
    
    class Meta:
        model = Edificacion
        fields = ['nombre_edificacion', 'propietario_de_la_edificacion', 'niveles_por_edificio', 'tipo_de_inmueble',
                  'superficie_construida_por_edificacion_m2', 'fecha_construccion_por_edificacion',
                  'caracteristicas_de_la_edificacion', 'usoEdificacion', 'calidadEdificacion',
                  'cajones_de_estacionamiento_por_edificacion', 'rampa_de_acceso', 'ruta_de_evacuacion',
                  'sanitario_para_personas_con_discapacidad']


class DocumentoPropiedadForm(forms.ModelForm):
    class Meta:
        model = DocumentoPropiedad
        fields = ['propietario_inmueble','institucion_propietario','superficie_amparada_m2','tipo_documento', 'numero_de_documento', 'fecha_creacion_DOC', 
                  'expedido_por', 'inscripcion_rppf', 'folio_real_federal', 'fecha_inscripcion_federal',
                  'inscripcion_registro_local', 'folio_real_local', 'folio_real_auxiliar', 'nombre_libro', 'tomo_o_volumen', 'numero', 'foja_o_folio', 'seccion', 'fecha_inscripcion_local',
                  'archivo'
                  ]
        
        widgets = {
            'fecha_creacion_DOC': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'fecha_inscripcion_federal': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'fecha_inscripcion_local': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['archivo'].widget.attrs.update({'class': 'form-control-file'})
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['propietario_inmueble'].initial = 'SIN INFORMACIÓN'
        self.fields['tipo_documento'].initial = 'SIN INFORMACIÓN'
        
        
class DatosAvaluosForm(forms.ModelForm):
    class Meta:
        model = DatosAvaluos
        fields = ['numero_de_avaluo', 'valor_de_avaluo', 'fecha_valor_de_avaluo', 'uso_del_avaluo', 'valor_de_terreno', 'valor_de_construccion']
        widgets = {
            'fecha_valor_de_avaluo': forms.DateInput(attrs={'type': 'date'}),
        }
        
class OcupacionesForm(forms.ModelForm):
    class Meta:
        model = Ocupaciones
        fields = (
            'tipo_procedimiento',
            'nombre_ocupante',
            'superficie_invadida',
            'no_expediente',
            'juzgado',
            'estatus_procedimiento',
            'suspension_acto',
            'recuperado',
            'fecha_recuperado'
        )
        
        
class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.folios_reales_form = FoliosRealesForm()
    class Meta:
        model = Task
        fields = [
                # Encabezado - Datos generales
                  'rfi', 'rfiProv', 'NombreInmueble', 'seccion_del_inventario', 'causa_alta', 'prioridad', 'Sector', 'Nombre_de_la_institucion_que_administra_el_inmueble', 'Naturaleza_Juridica_de_la_Institucion', 
                  'Denominaciones_anteriores', 'Dependencia_Administradora', 'subSeccion','certificado_de_seguridad', 'sentido_del_Dictamen', 
                  'descripcion_del_sentido_del_Dictamen','fecha_documento', 'subir_archivo','no_de_identificador_del_expediente_institucion', 
                # Ubicación
                  'pais', 'entidad_federativa', 'municipio_alcaldia', 'localidad', 'componente_espacial','fotografia_de_la_ubicacion',
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
                  'valor_construccion', 'valor_catastral_terreno', 'valor_catastral_construccion', 'valor_total_catastral', 'fecha_valor_catastral', 'documentacion_soporte' ]
        widgets = {
            'subir_archivo': CustomClearableFileInput,
            'fecha_documento': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'rfi': forms.TextInput(attrs={'disabled': 'disabled'}),
            'entidad_federativa': forms.Select(attrs={'onchange': "loadMunicipios(this.value);"}),  # Añadir el widget para el campo entidad_federativa
            'municipio_alcaldia': forms.Select,  # Añadir el widget para el campo municipio_alcaldia
            'fecha_valor_contable': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'fecha_valor_asegurable': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'fecha_valor_adquisicion': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'fecha_valor_catastral': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            
            
        }
        

from django.contrib.auth.models import User
class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['NombreInmueble', 'assigned_to', 'causa_alta', 'prioridad', 'deadline', 'Sector', 'Nombre_de_la_institucion_que_administra_el_inmueble']
        widgets = {
                'deadline': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa', 'type': 'date'}),
            }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        
        if not user.is_superuser:
            # Oculta el campo 'assigned_to' si el usuario no es superusuario
            self.fields['assigned_to'].widget = forms.HiddenInput()
            
            
            
class ColindanciasForm(ModelForm):
    class Meta:
        model = Colindancias
        fields = ['orientacion', 'colindancia', 'medida_en_metros']
            
class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['asunto', 'mensaje', 'enviar_a', 'enviado_por']  # Elimina 'enviado_por' ya que se llenará automáticamente
    enviar_a = forms.ModelChoiceField(queryset=User.objects.all(), label='Enviar A')



class PasswordConfirmationForm(forms.Form):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class SignInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    
    
    
class DocumentoOcupacionForm(forms.ModelForm):
    class Meta:
        model = Documento_ocupacion
        fields = 'tipo_de_documento', 'fecha_documento', 'inscripcion_RPPF', 'folio_real_federal', 'fecha_inscripcion_federal'
        widgets = {
            'fecha_documento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_inscripcion_federal': forms.DateInput(attrs={'type': 'date'}),
        }
        
class InstitucionesOcupantesForm(forms.ModelForm):
    class Meta:
        model = InstitucionesOcupantes
        fields = ['institucion_publica_ocupante', 'superficie_asignada', 'uso_institucion_ocupante', 'superficie_disponible']
        
class DatosTercerosForm(forms.ModelForm):
    class Meta:
        model = DatosTerceros
        fields = [
            'tipo_usuario_tercero',
            'beneficiario',
            'nombre_beneficiario',
            'rfc',
            'fecha_inicio_vigencia',
            'fecha_termino_vigencia',
            'prorroga',
            'inscripcion_folio_real_federal',
            'superficie_objeto_ocupacion_metros',
            'uso',
        ]

class TramitesDisposicionForm(forms.ModelForm):
    class Meta:
        model = TramitesDisposicion
        fields = ['tramite_disposicion', 'estatus', 'numero_de_expediente']

class BajaForm(forms.ModelForm):
    class Meta:
        model = Task
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
    
        
class Task_CONDIA_Form(forms.ModelForm):
    class Meta:
        model = Task_Condia
        fields = ['Nombre_inmueble']
        
        
class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = [
                # Encabezado - Datos generales
                  'rfi', 'rfiProv', 'NombreInmueble', 'seccion_del_inventario', 'causa_alta', 'prioridad', 'Sector', 'Nombre_de_la_institucion_que_administra_el_inmueble', 'Naturaleza_Juridica_de_la_Institucion', 
                  'Denominaciones_anteriores', 'Dependencia_Administradora', 'subSeccion','certificado_de_seguridad', 'sentido_del_Dictamen', 
                  'descripcion_del_sentido_del_Dictamen','fecha_documento', 'subir_archivo','no_de_identificador_del_expediente_institucion', 
                # Ubicación
                  'pais', 'entidad_federativa', 'municipio_alcaldia', 'localidad', 'componente_espacial','fotografia_de_la_ubicacion',
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
                  'valor_construccion', 'valor_catastral_terreno', 'valor_catastral_construccion', 'valor_total_catastral', 'fecha_valor_catastral', 'documentacion_soporte' ]
        widgets = {
            'subir_archivo': CustomClearableFileInput,
            'fecha_documento': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'rfi': forms.TextInput(attrs={'disabled': 'disabled'}),
            'entidad_federativa': forms.Select(attrs={'onchange': "loadMunicipios(this.value);"}),  # Añadir el widget para el campo entidad_federativa
            'municipio_alcaldia': forms.Select,  # Añadir el widget para el campo municipio_alcaldia
            'fecha_valor_contable': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'fecha_valor_asegurable': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'fecha_valor_adquisicion': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'fecha_valor_catastral': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
    }

class DocumentoOcupacionFormIMP(forms.ModelForm):
    class Meta:
        model = Documento_ocupacionIMP
        fields = 'tipo_de_documento', 'fecha_documento', 'inscripcion_RPPF', 'folio_real_federal', 'fecha_inscripcion_federal'
        widgets = {
            'fecha_documento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_inscripcion_federal': forms.DateInput(attrs={'type': 'date'}),
        }
        
class InstitucionesOcupantesFormIMP(forms.ModelForm):
    class Meta:
        model = InstitucionesOcupantesIMP
        fields = ['institucion_publica_ocupante', 'superficie_asignada', 'uso_institucion_ocupante', 'superficie_disponible']
        
class DatosTercerosFormIMP(forms.ModelForm):
    class Meta:
        model = DatosTercerosIMP
        fields = [
            'tipo_usuario_tercero',
            'beneficiario',
            'nombre_beneficiario',
            'rfc',
            'fecha_inicio_vigencia',
            'fecha_termino_vigencia',
            'prorroga',
            'inscripcion_folio_real_federal',
            'superficie_objeto_ocupacion_metros',
            'uso',
        ]

class TramitesDisposicionFormIMP(forms.ModelForm):
    class Meta:
        model = TramitesDisposicionIMP
        fields = ['tramite_disposicion', 'estatus', 'numero_de_expediente']

class ColindanciasFormIMP(ModelForm):
    class Meta:
        model = ColindanciasIMP
        fields = ['orientacion', 'colindancia', 'medida_en_metros']
        
class FoliosRealesFormIMP(forms.ModelForm):
    class Meta:
        model = FoliosRealesIMP
        fields = ['folios_reales_data']
        
class Numero_PlanoFormIMP(forms.ModelForm):
    class Meta:
        model = NumeroPlanoIMP
        fields = ['numero_plano_data']
        
class Expedientes_CEDOCFormIMP(forms.ModelForm):
    class Meta:
        model = Expedientes_CEDOCIMP
        fields = ['expediente_cedoc_data']
        
class Edificio_VerdeFormIMP(forms.ModelForm):
    class Meta:
        model = EdificioVerdeIMP
        fields = ['edificio_verde_data']

class EdificacionFormIMP(forms.ModelForm):
    
    class Meta:
        model = EdificacionIMP
        fields = ['nombre_edificacion', 'propietario_de_la_edificacion', 'niveles_por_edificio', 'tipo_de_inmueble',
                  'superficie_construida_por_edificacion_m2', 'fecha_construccion_por_edificacion',
                  'caracteristicas_de_la_edificacion', 'usoEdificacion', 'calidadEdificacion',
                  'cajones_de_estacionamiento_por_edificacion', 'rampa_de_acceso', 'ruta_de_evacuacion',
                  'sanitario_para_personas_con_discapacidad']


class DocumentoPropiedadFormIMP(forms.ModelForm):
    class Meta:
        model = DocumentoPropiedadIMP
        fields = ['propietario_inmueble','institucion_propietario','superficie_amparada_m2','tipo_documento', 'numero_de_documento', 'fecha_creacion_DOC', 
                  'expedido_por', 'inscripcion_rppf', 'folio_real_federal', 'fecha_inscripcion_federal',
                  'inscripcion_registro_local', 'folio_real_local', 'folio_real_auxiliar', 'nombre_libro', 'tomo_o_volumen', 'numero', 'foja_o_folio', 'seccion', 'fecha_inscripcion_local',
                  'archivo'
                  ]
        
        widgets = {
            'fecha_creacion_DOC': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'fecha_inscripcion_federal': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
            'fecha_inscripcion_local': forms.DateInput(attrs={'placeholder': 'dd/mm/aaa',}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['archivo'].widget.attrs.update({'class': 'form-control-file'})
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['propietario_inmueble'].initial = 'SIN INFORMACIÓN'
        self.fields['tipo_documento'].initial = 'SIN INFORMACIÓN'
        
        
class DatosAvaluosFormIMP(forms.ModelForm):
    class Meta:
        model = DatosAvaluosIMP
        fields = ['numero_de_avaluo', 'valor_de_avaluo', 'fecha_valor_de_avaluo', 'uso_del_avaluo', 'valor_de_terreno', 'valor_de_construccion']
        widgets = {
            'fecha_valor_de_avaluo': forms.DateInput(attrs={'type': 'date'}),
        }
        
class OcupacionesFormIMP(forms.ModelForm):
    class Meta:
        model = OcupacionesIMP
        fields = (
            'tipo_procedimiento',
            'nombre_ocupante',
            'superficie_invadida',
            'no_expediente',
            'juzgado',
            'estatus_procedimiento',
            'suspension_acto',
            'recuperado',
            'fecha_recuperado'
        )