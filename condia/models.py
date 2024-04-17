from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TareasCondia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField( null=True, blank=True)
    uso_inmueble = models.CharField(max_length=200, null=True, blank=True)
    riuf = models.CharField(max_length=200, null=True, blank=True)
    superficie_rentable = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    superficie_terreno = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    superficie_construida = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    personal_ocupante = models.IntegerField(null=True, blank=True)
    uso_suelo = models.CharField(max_length=200, null=True, blank=True)
    no_contrato = models.CharField(max_length=200, null=True, blank=True)
    fecha_firma_contrato = models.DateField(null=True, blank=True)
    monto_mensual_dictamen_estructural = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    correo1 = models.EmailField(null=True, blank=True)
    correo2 = models.EmailField(null=True, blank=True)
    razon_social = models.CharField(max_length=200, null=True, blank=True)
    propietario_representante = models.CharField(max_length=200, null=True, blank=True)
    identificacion_oficial = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    domicilio_fiscal = models.TextField(null=True, blank=True)
    justificacion_de_renta = models.TextField(null=True, blank=True)
    renta_mensual_civa_segun_contrato = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto_por_m2_civa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    
    ubicacion = models.CharField(max_length=200, null=True, blank=True)
    
    nombre_asentamiento = models.CharField(max_length=100, null=True, blank=True)
    codigo_postal = models.CharField(max_length=10, null=True, blank=True)
    entre_vialidades_referencia1 = models.CharField(max_length=100, null=True, blank=True)
    entre_vialidades_referencia2 = models.CharField(max_length=100, null=True, blank=True)
    vialidad_posterior = models.CharField(max_length=100, null=True, blank=True)
    descripcion_ubicacion = models.TextField(null=True, blank=True)
    fotoPresentacion = models.ImageField(upload_to='portadas/', blank=True, null=True)
    
    TIPO_DE_PROCESO_CHOICES = [
        ('Arrendamiento', 'Arrendamiento'),
        ('Legal', 'Legal'),
        ('Trámite de archivo', 'Trámite de archivo'),
    ]

    tipo_de_proceso = models.CharField(
        max_length=20,
        choices=TIPO_DE_PROCESO_CHOICES,
        default='Arrendamiento'
    )
    solicitud_espacio = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Solicitud de espacio o notificación a la UR")
    tabla_superficie_maxima = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Tabla de superficie máxima a ocupar por institución (SMOI)")
    justificacion_arrendamiento = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Justificación y autorización del arrendamiento ante el INDAABIN")
    solicitud_disponibilidad = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Solicitud de disponibilidad de inmuebles de propiedad federal y respuesta del INDAABIN")
    solicitud_arrendamiento_oficialia = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Solicitud y/o autorización del arrendamiento (Oficialía Mayor)")
    notificacion_propietario_arrendar = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Notificación al propietario para arrendar el inmueble")
    solicitud_justipreciacion_renta = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Solicitud de justipreciación de renta")
    notificacion_pago_derechos = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Notificación de pago de derechos del INDAABIN")
    dictamen_justipreciacion_renta = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Dictamen de justipreciación de renta")
    oficio_revision_juridica_respuesta = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Oficio de revisión jurídica y respuesta")
    justificacion_plurianual = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Justificación plurianual")
    oficio_solicitud_registro_obligacional = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Oficio de solicitud y registro obligacional (UAJ)")
    registro_contrato_pagina_indaabin = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Registro de contrato en página del INDAABIN")
    contrato_arrendamiento_convenios = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Contrato de arrendamiento y convenios")
    notificacion_ur_subdireccion_obras_planos = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Notificación a la UR y Subdirección de Obras para la elaboración de los planos de adecuación de oficinas")
    anexo_contrato_acta_recepcion_inmueble = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Anexo 1 al contrato de arrendamiento, acta-recepción del inmueble")
    documentos_inventario_condiciones = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Inventario y las condiciones de instalaciones y equipos propios del inmueble, validado por la Subdirección de Obras")
    documentos_dictamen_seguridad_estructural = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Dictamen de seguridad estructural emitido por un Director Responsable del Inmueble")
    documentos_usos_limitaciones = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Usos permitidos y en general todas las limitaciones derivadas de las características del inmueble")
    documentos_acta_entrega_trabajos = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Acta-Entrega de los trabajos de adecuación de oficinas a cargo de la Subdirección de obras")
    anexo_contrato_plano_distribucion_personal = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Anexo 2 al contrato de arrendamiento plano de distribución de personal (adecuación de oficinas autorizado)")
    notificacion_disponibilidad_ur = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Oficio de notificación de disponibilidad del inmueble a la UR")
    actas_entrega_asignacion_espacio = models.FileField(upload_to='Carpeta1Condia/', null=True, blank=True, verbose_name="Actas-entrega de asignación de espacio a las Unidades Administrativas")
    
    # Carpeta 2
    documentos_legales_escritura_inmueble = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Escritura del inmueble a arrendar (título de propiedad)")
    documentos_legales_acta_constitutiva = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Testimonio de la escritura pública que contenga el acta constitutiva de la empresa que tenga carácter de arrendador, tratándose de personas morales y Registro Público de la Propiedad y el Comercio")
    documentos_legales_escritura_cambio_regimen = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Escritura de cambio de régimen (si es el caso)")
    documentos_legales_poder_notarial = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Escritura pública que contenga el poder notarial de la persona que pretenda suscribir el contrato en representación del arrendado")
    documentos_legales_cedula_fiscal = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Cedula de identificación fiscal del arrendador, Registro Federal de Contribuyentes (RFC)")
    documentos_legales_identificacion_oficial = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Identificación oficial vigente con fotografía y firma del arrendador o representante legal, credencial de elector (INE)")
    documentos_legales_comprobante_domicilio_fiscal = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Comprobante de domicilio fiscal del arrendador")
    documentos_tecnicos_planos_arquitectonicos = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Planos Arquitectónicos")
    documentos_tecnicos_constancia_seguridad_estructural = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Registro de la constancia de seguridad estructural expedida por el GCDMX")
    documentos_tecnicos_visto_bueno_seguridad_operacion = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Visto bueno de seguridad y operción expedida por el GCDMX")
    documentos_tecnicos_ultimo_pago_predial = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Última boleta por concepto de pago del impuesto predial")
    documentos_tecnicos_ultimo_pago_agua = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Última boleta por concepto de suministro de agua potable")
    documentos_tecnicos_ultimo_pago_energia = models.FileField(upload_to='Carpeta2Condia/', null=True, blank=True, verbose_name="Último recibo por concepto de pago de servicio de energía eléctrica")
    fundamento_legal = models.FileField(upload_to='Carpeta3Condia/', null=True, blank=True, verbose_name="Fundamento Legal")
    class Meta:
        verbose_name = "Condia"
        verbose_name_plural = "Eventos"
        permissions = [
            ('add_CONDIA', 'Can add CONDIA in tasks app'),
            ('change_CONDIA', 'Can change CONDIA in tasks app'),
            ('delete_CONDIA', 'Can delete CONDIA in tasks app'),
            ('view_CONDIA', 'Can view CONDIA in tasks app'),
        ]

    def __str__(self):
        return f"Tarea: {self.titulo}"

from django.db import models

