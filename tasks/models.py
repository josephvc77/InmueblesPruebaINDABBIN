from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
import os

@deconstructible
class TaskFilePath(object):
    def __call__(self, instance, filename):
        # Genera la ruta para guardar el archivo en la carpeta 'uploads'
        return os.path.join('uploads', filename)
    
@deconstructible
class InmueblesFiles(object):
    def __call__(self, instance, filename):
        # Genera la ruta para guardar el archivo en la carpeta 'uploads'
        return os.path.join('uploads/importados', filename)



class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
 

class Inmueble(models.Model):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='assigned_inmueble')
    NombreInmueble = models.CharField(max_length=100, verbose_name='Nombre del inmueble', null=True, blank=True)
    rfi = models.CharField(max_length=15, null=True, blank=True)
    CHOICES = (
    ('Si', 'Si'),
    ('No', 'No'),
)

    rfiProv = models.CharField(
    max_length=4,
    choices=CHOICES,
    default='No', null=True, blank=True
)
    
    UR_CHOICES = [
        ('CGEE', 'CGEE'),
        ('DGB', 'DGB'),
        ('DGBTEPD', 'DGBTEPD'),
        ('DGCFT', 'DGCFT'),
        ('DGETAyCM', 'DGETAyCM'),
        ('DGETI', 'DGETI'),
        ('DGRMyS', 'DGRMyS'),
        ('RESEMS', 'RESEMS'),
    ]
    UR = models.CharField(max_length=30, choices=UR_CHOICES, null=True, blank=True)
    
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Baja', 'Baja'),
        ('Completado', 'Completado'),
    ]
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Activo', null=True, blank=True)
    seccion_del_inventario = models.CharField(max_length=100, null=True, blank=True)
    
    deadline = models.DateTimeField(null=True, blank=True)
   
    Dependencia_Administradora = models.CharField(max_length=100, null=True, blank=True)
    
    SECTOR_INSTITUCION_CHOICES = [
        ('SECRETARÍA DE EDUCACIÓN PÚBLICA', 'SECRETARÍA DE EDUCACIÓN PÚBLICA'),
    ]
    Sector = models.CharField(max_length=100, choices=SECTOR_INSTITUCION_CHOICES, null=True, blank=True)
    
    
    
   
    NOMBRE_INSTITUCION_CHOICES = [
        ('SECRETARÍA DE EDUCACIÓN PÚBLICA', 'SECRETARÍA DE EDUCACIÓN PÚBLICA'),
    ]
    Nombre_de_la_institucion_que_administra_el_inmueble = models.CharField(max_length=100, choices=NOMBRE_INSTITUCION_CHOICES,  null=True, blank=True)
    
    subSeccion= models.CharField(max_length=100, null=True, blank=True)
    
    NATURALEZA_JURIDICA_CHOICES = [
        ('DEPENDENCIA', 'DEPENDENCIA'),
    ]
    Naturaleza_Juridica_de_la_Institucion = models.CharField(max_length=100, choices=NATURALEZA_JURIDICA_CHOICES, default='DEPENDENCIA',  null=True, blank=True)
    causa_alta_choices = [
        ('SIN INFORMACION', 'SIN INFORMACION'),
        ('POR ADQUISICION DEL INMUEBLE', 'POR ADQUISICION DEL INMUEBLE'),
        ('CUANDO SE HAYA OMITIDO DAR DE ALTA UN INMUEBLE FEDERAL', 'CUANDO SE HAYA OMITIDO DAR DE ALTA UN INMUEBLE FEDERAL'),
        ('POR INFORMACION FEHACIENTE CONTENIDA EN LOS ACERVOS DEL SIIFP', 'POR INFORMACION FEHACIENTE CONTENIDA EN LOS ACERVOS DEL SIIFP'),
        ('EN CASO DE QUE SE TENGA CONOCIMIENTO DE QUE UN INMUEBLE ES FEDERAL EN TERMINOS DE LA LEY', 'EN CASO DE QUE SE TENGA CONOCIMIENTO DE QUE UN INMUEBLE ES FEDERAL EN TERMINOS DE LA LEY'),
    ]
    
    causa_alta = models.CharField(max_length=100, choices=causa_alta_choices, default='SIN INFORMACION',  null=True, blank=True)
    
    PRIORIDAD_CHOICES = [('Alta', 'Alta'), ('Media', 'Media'),('Baja', 'Baja') ]
    
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='Media', null=True, blank=True)

    Denominaciones_anteriores = models.CharField(max_length=400,  null=True, blank=True)
    creado = models.CharField(max_length=20,null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    subir_archivo = models.FileField(upload_to=InmueblesFiles(), blank=True, null=True, editable=True)
    
    # Encabezazdo
    CERTIFICADO_OPCIONES = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    certificado_de_seguridad = models.CharField(max_length=4, choices=CERTIFICADO_OPCIONES, default='Si',  null=True, blank=True)

    SENTIDO_DICTAMEN_OPCIONES = [
        ('Inmueble Seguro', 'Inmueble Seguro'),
        ('Inmueble con daños menores que pueden repararse', 'Inmueble con daños menores que pueden repararse'),
        ('Inmueble con Daño estructural', 'Inmueble con Daño estructural'),
        ('Otros', 'Otros'),
    ]
    sentido_del_Dictamen = models.CharField(max_length=100, choices=SENTIDO_DICTAMEN_OPCIONES, default='Inmueble Seguro',  null=True, blank=True)
    
    descripcion_del_sentido_del_Dictamen = models.TextField(null=True, blank=True)
    fecha_documento = models.DateField(null=True, blank=True)
    no_de_identificador_del_expediente_institucion = models.CharField(max_length=100,  null=True, blank=True)


    # Nuevos campos para la sección de Ubicación
    pais_choices = [
        ('MÉXICO', 'MÉXICO'),
        # Otras opciones para países si las necesitas
    ]
    pais = models.CharField(max_length=100, choices=pais_choices, default='MÉXICO', null=True, blank=True)

    # Otros campos existentes...

    entidad_federativa = models.CharField(max_length=100, blank=True, null=True)
    municipio_alcaldia = models.CharField(max_length=100, blank=True, null=True)
    municipio_no_existente = models.CharField(max_length=120, blank=True, null=True)
    localidad = models.CharField(max_length=100, null=True, blank=True)
    fotografia_de_la_ubicacion = models.ImageField(upload_to='ubicacion_photos/', blank=True, null=True)
    COMPONENTE_ESPACIAL_CHOICES = [
        ('SIN INFORMACION', 'Sin Información'),
        ('CAMINO', 'Camino'),
        ('CARRETERA', 'Carretera'),
        ('ISLA', 'Isla'),
        ('VIALIDAD', 'Vialidad'),
    ]
    componente_espacial = models.CharField(max_length=150, choices=COMPONENTE_ESPACIAL_CHOICES, default='SIN INFORMACION',  null=True, blank=True)

    TIPO_VIALIDAD_CHOICES = [
        ('SIN INFORMACION', 'Sin Información'),
        ('AMPLIACIÓN', 'Ampliación'),
        ('ANDADOR', 'Andador'),
        ('AVENIDA', 'Avenida'),
        ('BOULEVARD', 'Boulevard'),
        ('CALLE', 'Calle'),
        ('CALLEJÓN', 'Callejón'),
        ('CALZADA', 'Calzada'),
        ('CERRADA', 'Cerrada'),
        ('CIRCUITO', 'Circuito'),
        ('CIRCUNVALACIÓN', 'Circunvalación'),
        ('CONTINUACIÓN', 'Continuación'),
        ('CORREDOR', 'Corredor'),
        ('DIAGONAL', 'Diagonal'),
        ('EJE VIAL', 'Eje Vial'),
        ('PASAJE', 'Pasaje'),
        ('PEATONAL', 'Peatonal'),
        ('PERIFÉRICO', 'Periférico'),
        ('PRIVADA', 'Privada'),
        ('PROLONGACIÓN', 'Prolongación'),
        ('RETORNO', 'Retorno'),
        ('VIADUCTO', 'Viaducto'),
    ]
    tipo_vialidad = models.CharField(max_length=150, choices=TIPO_VIALIDAD_CHOICES, default='SIN INFORMACION',  null=True, blank=True)

    nombre_vialidad = models.CharField(max_length=100,  null=True, blank=True)
    numero_exterior = models.CharField(max_length=240,  null=True, blank=True)
    numero_exterior_2 = models.CharField(max_length=240, null=True, blank=True)
    numero_interior = models.CharField(max_length=240, null=True, blank=True)
    TIPO_ASENTAMIENTO_CHOICES = [
        ('SIN INFORMACIÓN', 'Sin Información'),
        ('AEROPUERTO', 'Aeropuerto'),
        ('AMPLIACIÓN', 'Ampliación'),
        ('BARRIO', 'Barrio'),
        ('CANTÓN', 'Cantón'),
        ('CIUDAD', 'Ciudad'),
        ('CIUDAD INDUSTRIAL', 'Ciudad Industrial'),
        ('COLONIA', 'Colonia'),
        ('CONDOMINIO', 'Condominio'),
        ('CONJUNTO HABITACIONAL', 'Conjunto Habitacional'),
        ('CORREDOR INDUSTRIAL', 'Corredor Industrial'),
        ('COTO', 'Coto'),
        ('CUARTEL', 'Cuartel'),
        ('EJIDO', 'Ejido'),
        ('EXHACIENDA', 'Exhacienda'),
        ('FRACCIÓN', 'Fracción'),
        ('FRACCIONAMIENTO', 'Fraccionamiento'),
        ('GRANJA', 'Granja'),
        ('HACIENDA', 'Hacienda'),
        ('INGENIO', 'Ingenio'),
        ('ISLA', 'Isla'),
        ('MANZANA', 'Manzana'),
        ('PARAJE', 'Paraje'),
        ('PARQUE INDUSTRIAL', 'Parque Industrial'),
        ('PRIVADA', 'Privada'),
        ('PROLONGACIÓN', 'Prolongación'),
        ('PUEBLO', 'Pueblo'),
        ('PUERTO', 'Puerto'),
        ('RANCHERIA', 'Ranchería'),
        ('RANCHO', 'Rancho'),
        ('REGIÓN', 'Región'),
        ('RESIDENCIAL', 'Residencial'),
        ('RINCONADA', 'Rinconada'),
        ('SECCIÓN', 'Sección'),
        ('SECTOR', 'Sector'),
        ('SUPERMANZANA', 'Supermanzana'),
        ('UNIDAD', 'Unidad'),
        ('UNIDAD HABITACIONAL', 'Unidad Habitacional'),
        ('VILLA', 'Villa'),
        ('ZONA FEDERAL', 'Zona Federal'),
        ('ZONA INDUSTRIAL', 'Zona Industrial'),
        ('ZONA MILITAR', 'Zona Militar'),
        ('ZONA NAVAL', 'Zona Naval'),
    ]
    tipo_asentamiento = models.CharField(max_length=130, choices=TIPO_ASENTAMIENTO_CHOICES, default='SIN INFORMACIÓN',  null=True, blank=True)

    nombre_asentamiento = models.CharField(max_length=100,  null=True, blank=True)
    codigo_postal = models.CharField(max_length=40,  null=True, blank=True)
    entre_vialidades_referencia1 = models.CharField(max_length=100,  null=True, blank=True)
    entre_vialidades_referencia2 = models.CharField(max_length=100,  null=True, blank=True)
    vialidad_posterior = models.CharField(max_length=100,  null=True, blank=True)
    descripcion_ubicacion = models.TextField(null=True, blank=True)
    
    DATUM_CHOICES = (
        ('SIN INFORMACIÓN', 'SIN INFORMACIÓN'),
        ('ITRF1008', 'ITRF1008'),
        ('ITRF92', 'ITRF92'),
        ('NAD27', 'NAD27'),
        ('WGS84', 'WGS84'),
    )

    datum = models.CharField(max_length=100, choices=DATUM_CHOICES, null=True, blank=True)
    utmx = models.CharField(max_length=100, blank=True, null=True)
    utmy = models.CharField(max_length=100, blank=True, null=True)
    utm_zona = models.CharField(max_length=100, blank=True, null=True)
    latitud = models.CharField(max_length=100, blank=True, null=True)
    longitud = models.CharField(max_length=100, blank=True, null=True)
    
     # Campos relacionados con Edificación
    NOMBRE_EDIFICACION_CHOICES = [
        ('Sin informacion', 'Sin Información'),
        ('Edificacion', 'Edificación'),
        ('Mixto', 'Mixto'),
        ('Terreno', 'Terreno'),
    ]
    
    superficie_del_terreno_en_M2 = models.CharField(max_length=100, null=True, blank=True)
    superficie_del_terreno_HA = models.CharField(max_length=100, null=True, blank=True)
    superficie_de_desplante_en_M2 = models.CharField(max_length=100, null=True, blank=True)
    superficie_construida_en_M2 = models.CharField(max_length=100, null=True, blank=True)
       # Opciones para los campos de selección
    ZONA_CHOICES = (
        ('sin informacion', 'Sin Información'),
        ('rural', 'Rural'),
        ('semiurbana', 'Semiurbana'),
        ('urbana', 'Urbana'),
    )

    CALIDAD_CHOICES = (
        ('sin informacion', 'Sin Información'),
        ('buena', 'Buena'),
        ('de_lujo', 'De Lujo'),
        ('economica', 'Económica'),
        ('media', 'Media'),
        ('muy_buena', 'Muy Buena'),
        ('otro', 'Otro'),
    )

    SERVICIOS_CHOICES = (
        ('sin informacion', 'Sin Información'),
        ('basicos', 'Básicos'),
        ('completos', 'Completos'),
        ('escasos', 'Escasos'),
        ('sin_servicios', 'Sin Servicios'),
    )

    ESTADO_CONSERVACION_CHOICES = (
        ('seleccionar estado', 'Seleccionar el Estado de Conservación'),
        ('excelente', 'Excelente'),
        ('bueno', 'Bueno'),
        ('regular', 'Regular'),
        ('malo', 'Malo'),
        ('ruinoso', 'Ruinoso'),
        ('muy_bueno', 'Muy Bueno'),
    )

    # Caracteristicas
    superficie_util_m2 = models.CharField(max_length=150, null=True, blank=True)
    zona_ubicacion = models.CharField(max_length=100, choices=ZONA_CHOICES, null=True, blank=True, default='Sin Información')
    calidad_construccion = models.CharField(max_length=100, choices=CALIDAD_CHOICES, null=True, blank=True, default='Sin Información')
    servicios = models.CharField(max_length=100, choices=SERVICIOS_CHOICES, null=True, blank=True, default='Sin Información')
    telefono_inmueble = models.CharField(max_length=150, null=True, blank=True)
    fecha_inicio_construccion = models.DateField(null=True, blank=True)
    siglo_construccion = models.CharField( max_length=100,null=True, blank=True)
    fecha_ultima_remodelacion = models.DateField(null=True, blank=True)
    MONUMENTO_CHOICES = (
        ('SI', 'SI'),
        ('No', 'No'),
    )
    monumento = models.CharField(max_length=4, choices=MONUMENTO_CHOICES, null=True, blank=True, default='No')

    HISTORICO_CHOICES = (
        ('SI', 'SI'),
        ('No', 'No'),
    )
    historico = models.CharField(max_length=4, choices=HISTORICO_CHOICES, null=True, blank=True, default='No')

    ARTISTICO_CHOICES = (
        ('SI', 'SI'),
        ('No', 'No'),
    )
    artistico = models.CharField(max_length=4, choices=ARTISTICO_CHOICES, null=True, blank=True, default='No')

    ARQUEOLOGICO_CHOICES = (
        ('SI', 'SI'),
        ('No', 'No'),
    )
    arqueologico = models.CharField(max_length=4, choices=ARQUEOLOGICO_CHOICES, null=True, blank=True, default='No')
    
    clave_inah = models.CharField(max_length=100, null=True, blank=True)
    folio_real_inah = models.CharField(max_length=100, null=True, blank=True)
    no_plano_inah = models.CharField(max_length=100, null=True, blank=True)
    clave_cnmh = models.CharField(max_length=100, null=True, blank=True)
    clave_dgsmpc_conaculta = models.CharField(max_length=100, null=True, blank=True)
    fecha_inscripcion_unesco = models.CharField(max_length=100 ,null=True, blank=True)
    observaciones_historicas = models.TextField(null=True, blank=True)
    siglo_o_periodo = models.CharField(max_length=100, null=True, blank=True)
    correlativo = models.CharField(max_length=100, null=True, blank=True)
    conjunto = models.CharField(max_length=100, null=True, blank=True)
    clave_inbal = models.CharField(max_length=100, null=True, blank=True)
    registro_unico_inah = models.CharField(max_length=100, null=True, blank=True)
    

    estado_conservacion = models.CharField(max_length=100, choices=ESTADO_CONSERVACION_CHOICES, null=True, blank=True)
    
    TIPO_INMUEBLE_RURAL_CHOICES = [
        ("SIN INFORMACIÓN", "SIN INFORMACIÓN"),
        ("AGOSTADERO", "AGOSTADERO"),
        ("RIEGO", "RIEGO"),
        ("TEMPORAL", "TEMPORAL"),
    ]
    tipo_inmueble_rural = models.CharField(
        max_length=100,
        choices=TIPO_INMUEBLE_RURAL_CHOICES,
        default="SIN INFORMACIÓN" , null=True, blank=True
    )

    USO_DOMINANTE_ZONA_CHOICES = [
        ("SIN INFORMACION", "SIN INFORMACIÓN"),
        ("COMERCIAL", "COMERCIAL"),
        ("DE OFICINAS", "DE OFICINAS"),
        ("HABITACIONAL", "HABITACIONAL"),
        ("INDUSTRIAL", "INDUSTRIAL"),
        ("OTRO", "OTRO"),
    ]
    uso_dominante_zona = models.CharField(
        max_length=100,
        choices=USO_DOMINANTE_ZONA_CHOICES,
        default="SIN INFORMACIÓN", null=True, blank=True
    )
    
    CLASIFICACION_EDAD_CHOICES = [
        ("SIN CLASIFICACIÓN", "SIN CLASIFICACIÓN"),
        ("ANTIGUO", "ANTIGUO"),
        ("MODERNO", "MODERNO"),
    ]
    clasificacion_edad = models.CharField(
        max_length=100,
        choices=CLASIFICACION_EDAD_CHOICES,
        default="SIN CLASIFICACIÓN", null=True, blank=True
    )

    CATEGORIA_CHOICES = [
        ("SIN CATEGORÍA", "SIN CATEGORÍA"),
        ("CON PLAZAS Y COMERCIOS", "CON PLAZAS Y COMERCIOS"),
        ("DE ABASTO", "DE ABASTO"),
        ("DE LUJO", "DE LUJO"),
        ("DE PRIMER ORDEN", "DE PRIMER ORDEN"),
        ("DE SEGUNDO ORDEN", "DE SEGUNDO ORDEN"),
        ("DE TERCER ORDEN", "DE TERCER ORDEN"),
        ("EN TRANSICIÓN", "EN TRANSICIÓN"),
        ("OTRO", "OTRO"),
    ]
    categoria = models.CharField(
        max_length=100,
        choices=CATEGORIA_CHOICES,
        default="SIN CATEGORÍA", null=True, blank=True
    )
    
    GRADO_CONSOLIDACION_CHOICES = [
        ("SIN INFORMACIÓN", "SIN INFORMACIÓN"),
        ("CONSOLIDADO", "CONSOLIDADO"),
        ("EN DECLINACIÓN", "EN DECLINACIÓN"),
        ("EN DESARROLLO", "EN DESARROLLO"),
        ("EN PROCESO DE CONSOLIDACIÓN", "EN PROCESO DE CONSOLIDACIÓN"),
        ("EN RENOVACIÓN", "EN RENOVACIÓN"),
        ("OTRO", "OTRO"),
    ]
    grado_consolidacion = models.CharField(
        max_length=100,
        choices=GRADO_CONSOLIDACION_CHOICES,
        default="SIN INFORMACIÓN", null=True, blank=True
    )
    
    # ---------------------------- campos Uso ----------------------------------------------------
    usuario_principal_del_inmueble = models.CharField(max_length=355, null=True, blank=True)
    usoGenerico = models.CharField(max_length=355, null=True, blank=True)
    usoEspecifico = models.CharField(max_length=355, null=True, blank=True)
    
    UsoSueloChoice = [
        ("SIN INFORMACIÓN", "SIN INFORMACIÓN"),
        ("AGOSTADERO (ZONA DE PASTOREO)", "AGOSTADERO (ZONA DE PASTOREO)"),
        ("AGRÍCOLA CON INSTALACIONES PARA RIEGO", "AGRÍCOLA CON INSTALACIONES PARA RIEGO"),
        ("AGRÍCOLA DE TEMPORAL (SIN INSTALACIONES PARA RIEGO)", "AGRÍCOLA DE TEMPORAL (SIN INSTALACIONES PARA RIEGO)"),
        ("ÁREAS NATURALES PROTEGIDAS (RESERVAS DE LA BIÓSFERA O SIMILAR)", "ÁREAS NATURALES PROTEGIDAS (RESERVAS DE LA BIÓSFERA O SIMILAR)"),
        ("COMERCIAL Y/O OFICINAS CALIDAD BUENA", "COMERCIAL Y/O OFICINAS CALIDAD BUENA"),
        ("COMERCIAL Y/O OFICINAS CALIDAD MEDIA", "COMERCIAL Y/O OFICINAS CALIDAD MEDIA"),
        ("COMERCIAL Y/O OFICINAS DE LUJO", "COMERCIAL Y/O OFICINAS DE LUJO"),
        ("COMERCIAL Y/U OFICINAS CALIDAD POPULAR", "COMERCIAL Y/U OFICINAS CALIDAD POPULAR"),
        ("COMERCIAL Y/U OFICINAS LUJO ZONAS METROPOLITANAS", "COMERCIAL Y/U OFICINAS LUJO ZONAS METROPOLITANAS"),
        ("EQUIPAMIENTO RURAL CENTROS DE READAPTACIÓN SOCIAL (CEFERESOS, CERESOS, CÁRCELES)", "EQUIPAMIENTO RURAL CENTROS DE READAPTACIÓN SOCIAL (CEFERESOS, CERESOS, CÁRCELES)"),
        ("EQUIPAMIENTO RURAL PUERTO FRONTERIZO", "EQUIPAMIENTO RURAL PUERTO FRONTERIZO"),
        ("EQUIPAMIENTO RURAL TRANSPORTE AIRE O TIERRA", "EQUIPAMIENTO RURAL TRANSPORTE AIRE O TIERRA"),
        ("EQUIPAMIENTO RURAL ZONAS MILITARES O NAVALES, EQUIPAMIENTO INDUSTRIAL, ENERGÉTICO", "EQUIPAMIENTO RURAL ZONAS MILITARES O NAVALES, EQUIPAMIENTO INDUSTRIAL, ENERGÉTICO"),
        ("EQUIPAMIENTO URBANO CENTROS DE READAPTACIÓN SOCIAL (CEFERESOS, CERESOS, CÁRCELES)", "EQUIPAMIENTO URBANO CENTROS DE READAPTACIÓN SOCIAL (CEFERESOS, CERESOS, CÁRCELES)"),
        ("EQUIPAMIENTO URBANO PALACIO FEDERAL, PUERTO FRONTERIZO", "EQUIPAMIENTO URBANO PALACIO FEDERAL, PUERTO FRONTERIZO"),
        ("EQUIPAMIENTO URBANO SERVICIOS DE ABASTO, MERCADOS", "EQUIPAMIENTO URBANO SERVICIOS DE ABASTO, MERCADOS"),
        ("EQUIPAMIENTO URBANO SERVICIOS EDUCATIVOS, SALUD, CULTURA, DEPORTE, TURÍSTICOS", "EQUIPAMIENTO URBANO SERVICIOS EDUCATIVOS, SALUD, CULTURA, DEPORTE, TURÍSTICOS"),
        ("EQUIPAMIENTO URBANO TRANSPORTE AIRE O TIERRA, ESTACIONAMIENTOS CUBIERTOS", "EQUIPAMIENTO URBANO TRANSPORTE AIRE O TIERRA, ESTACIONAMIENTOS CUBIERTOS"),
        ("EQUIPAMIENTO URBANO ZONAS MILITARES O NAVALES, EQUIPAMIENTO INDUSTRIAL, ENERGÉTICO", "EQUIPAMIENTO URBANO ZONAS MILITARES O NAVALES, EQUIPAMIENTO INDUSTRIAL, ENERGÉTICO"),
        ("EQUIPAMIENTO ZONA RURAL (HOSPITAL, TRANPORTE AIRE O TIERRA, MILITAR O NAVAL, PTO. FRONTERIZO, SERV)", "EQUIPAMIENTO ZONA RURAL (HOSPITAL, TRANPORTE AIRE O TIERRA, MILITAR O NAVAL, PTO. FRONTERIZO, SERV)"),
        ("HABITACIONAL CALIDAD BUENA", "HABITACIONAL CALIDAD BUENA"),
        ("HABITACIONAL CALIDAD MEDIA", "HABITACIONAL CALIDAD MEDIA"),
        ("HABITACIONAL CALIDAD POPULAR", "HABITACIONAL CALIDAD POPULAR"),
        ("HABITACIONAL RURAL", "HABITACIONAL RURAL"),
        ("HABITACIONAL Y/U OFICINAS RURAL", "HABITACIONAL Y/U OFICINAS RURAL"),
        ("INDUSTRIA ACUÍCOLA", "INDUSTRIA ACUÍCOLA"),
        ("INDUSTRIA AGROPECUARIA", "INDUSTRIA AGROPECUARIA"),
        ("INDUSTRIAL CALIDAD BUENA", "INDUSTRIAL CALIDAD BUENA"),
        ("INDUSTRIAL CALIDAD POPULAR", "INDUSTRIAL CALIDAD POPULAR"),
        ("INDUSTRIAL RURAL (ALMACENAMIENTO)", "INDUSTRIAL RURAL (ALMACENAMIENTO)"),
        ("ZONA RURAL ÁREAS VERDES PROTECCIÓN AMBIENTAL, VIVEROS FORESTALES", "ZONA RURAL ÁREAS VERDES PROTECCIÓN AMBIENTAL, VIVEROS FORESTALES"),
        ("ZONA URBANA ÁREAS VERDES, ESPACIOS ABIERTOS, DEPORTIVOS, PARQUES, PLAZAS, VIVEROS", "ZONA URBANA ÁREAS VERDES, ESPACIOS ABIERTOS, DEPORTIVOS, PARQUES, PLAZAS, VIVEROS"),
    ]
    
    uso_de_suelo_autorizado = models.CharField(max_length=355, choices=UsoSueloChoice, default="SIN INFORMACIÓN", null=True, blank=True)
    
    
    numero_de_empleados_en_el_inmueble = models.CharField(max_length=100, null=True, blank=True)
    DOCUMENTO_OCUPACION_CHOICEONES = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    documento_que_autoriza_ocupacion = models.CharField(max_length=4, choices=DOCUMENTO_OCUPACION_CHOICEONES, default='No',  null=True, blank=True)
    numero_de_documentos_de_ocupacion = models.CharField(max_length=100, null=True, blank=True)
    INSTITUCIONES_OCUPANTES_CHOICE = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    instituciones_ocupantes = models.CharField(max_length=4, choices=INSTITUCIONES_OCUPANTES_CHOICE, default='No',  null=True, blank=True)
    USUARIOS_TERCEROS_CHOICE = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    usuarios_terceros = models.CharField(max_length=4, choices=USUARIOS_TERCEROS_CHOICE, default='No',  null=True, blank=True)
    
    
    #------------------------------------ campos aprovechamiento---------------------------------------
    
    APROVECHAMIENTO_CHOICES = [
        ('SIN INFORMACIÓN', 'SIN INFORMACIÓN'),
        ('APROVECHABLE', 'APROVECHABLE'),
        ('APROVECHADO', 'APROVECHADO'),
        ('NO APROVECHABLE', 'NO APROVECHABLE'),
        ('NO APROVECHADO', 'NO APROVECHADO'),
    ]
    
    aprovechamiento = models.CharField(max_length=100, choices=APROVECHAMIENTO_CHOICES, default='SIN INFORMACIÓN', null=True, blank=True)
    
    inmueble_con_atencion_al_publico_choice = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    inmueble_con_atencion_al_publico = models.CharField(max_length=5, choices=inmueble_con_atencion_al_publico_choice, null=True, blank=True)
    
    
    poblacion_beneficiada = models.CharField(max_length=100, null=True, blank=True)
    poblacion_servicio = models.CharField(max_length=100, null=True, blank=True)
    cuenta_con_proyecto_de_uso_inmediato_desarrollado_choice = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    cuenta_con_proyecto_de_uso_inmediato_desarrollado = models.CharField(max_length=100, choices=cuenta_con_proyecto_de_uso_inmediato_desarrollado_choice, null=True, blank=True)
    
    
    inversion_requerida = models.CharField(max_length=100, null=True, blank=True)
    fuente_financiamiento = models.CharField(max_length=100, null=True, blank=True)
    fecha_solicitud = models.CharField(max_length=100 ,null=True, blank=True)
    
    inmueble_no_aprovechable_especificar = models.TextField(null=True, blank=True)
    
    gasto_anual_de_mantenimiento = models.CharField(max_length=100, null=True, blank=True)
    inmueble_en_condominio_choice = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    inmueble_en_condominio = models.CharField(max_length=20, choices=inmueble_en_condominio_choice, null=True, blank=True)
    
    superficie_total = models.CharField(max_length=100, null=True, blank=True)
    indiviso = models.CharField(max_length=100, null=True, blank=True)
    
    # -------------------------------- campos Valor ------------------------------------------------------------------
    valor_contable = models.CharField(max_length=100, null=True, blank=True)
    fecha_valor_contable = models.CharField(max_length=100 ,null=True, blank=True)
    valor_asegurable = models.CharField(max_length=100, null=True, blank=True)
    fecha_valor_asegurable = models.CharField(max_length=100 ,null=True, blank=True)
    valor_adquisicion = models.CharField(max_length=100, null=True, blank=True)
    fecha_valor_adquisicion = models.CharField(max_length=100 ,null=True, blank=True)
    valor_terreno = models.CharField(max_length=100, null=True, blank=True)
    valor_construccion = models.CharField(max_length=100, null=True, blank=True)
    valor_catastral_terreno = models.CharField(max_length=100, null=True, blank=True)
    valor_catastral_construccion = models.CharField(max_length=100, null=True, blank=True)
    valor_total_catastral = models.CharField(max_length=100, null=True, blank=True)
    fecha_valor_catastral = models.CharField(max_length=100 ,null=True, blank=True)
    documentacion_soporte = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name = "Inmueble Importado"
        verbose_name_plural = "Inmuebles Importados"
        
class DictamenEstructuralIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='dictamen_estructural')
    no_de_identificador_del_expediente_institucion = models.CharField(max_length=100, unique=True, null=True, blank=False)
    subir_archivo_dictamen = models.FileField(upload_to='Dictamen-Estructurales/', blank=True, null=True, editable=True)
    certificado_de_seguridad = models.CharField(max_length=4, null=True, blank=False)
    sentido_del_Dictamen = models.CharField(max_length=100, null=True, blank=False)
    descripcion_del_sentido_del_Dictamen = models.TextField(null=True, blank=False)
    fecha_documento = models.DateField(null=True, blank=False)
    

    
class FoliosRealesIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='folios_reales')
    folios_reales_data = models.CharField(max_length=100, unique=True, null=True, blank=False)
    archivo_folios_reales = models.FileField(upload_to='FoliosReales/', blank=True, null=True, editable=True)
    
class NumeroPlanoIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='numeros_planos')
    numero_plano_data = models.CharField(max_length=10, null=True, unique=True)
    archivo_Numero_Plano = models.FileField(upload_to='NumerosPlanos/', blank=True, null=True, editable=True)
 

    
class Expedientes_CEDOCIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='expedientes_deoc')
    expediente_cedoc_data = models.CharField(max_length=100, unique=True, null=True)
    archivo_Expedientes_CEDOC = models.FileField(upload_to='Expedientes-CEDOC/', blank=True, null=True, editable=True)

   
    
class EdificioVerdeIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE,  related_name='edificio_verde_set')
    OPCIONES_EDIFICIO_VERDE = [
        ('SIN INFORMACIÓN', 'SIN INFORMACIÓN'),
        ('SISTEMAS DE CAPTACIÓN DE AGUA PLUVIAL', 'SISTEMAS DE CAPTACIÓN DE AGUA PLUVIAL'),
        ('FUENTES DE ENERGÍA ALTERNAS', 'FUENTES DE ENERGÍA ALTERNAS'),
        ('AZOTEAS Y MUROS VERDES', 'AZOTEAS Y MUROS VERDES'),
        ('OPTIMIZACIÓN DE ESPACIOS (ELEVADORES DE AUTOS)', 'OPTIMIZACIÓN DE ESPACIOS (ELEVADORES DE AUTOS)'),
        ('SISTEMAS AUTOMATIZADOS DE ILUMINACIÓN', 'SISTEMAS AUTOMATIZADOS DE ILUMINACIÓN'),
        ('MATERIALES DE CONSTRUCCIÓN SUSTENTABLES', 'MATERIALES DE CONSTRUCCIÓN SUSTENTABLES'),
        ('TRATAMIENTO DE AGUAS GRISES', 'TRATAMIENTO DE AGUAS GRISES'),
    ]

    edificio_verde_data = models.CharField(max_length=50, choices=OPCIONES_EDIFICIO_VERDE, null=True, blank=True)
    
    def __str__(self):
        return self.edificio_verde_data

    

class EdificacionIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='edificaciones')
    tipo_de_inmueble_choices = [
        ('SIN INFORMACION', 'Sin Información'),
        ('EDIFICACION', 'Edificación'),
        ('MIXTO', 'Mixto'),
        ('TERRENO', 'Terreno'),
    ]
    tipo_de_inmueble = models.CharField(max_length=20, choices=tipo_de_inmueble_choices, default='SIN INFORMACION')
    nombre_edificacion = models.CharField(max_length=100, null=True, blank=True)
    propietario_de_la_edificacion = models.CharField(max_length=100, null=True, blank=True)
    niveles_por_edificio = models.CharField(max_length=100, null=True, blank=True)
    superficie_construida_por_edificacion_m2 = models.CharField(max_length=100, null=True, blank=True)
    fecha_construccion_por_edificacion = models.DateField(null=True, blank=True)
    caracteristicas_de_la_edificacion = models.TextField(null=True, blank=True)
    usoEdificacion = models.CharField(max_length=100, null=True, blank=True)
    calidadEdificacion = models.CharField(max_length=100, null=True, blank=True)
    cajones_de_estacionamiento_por_edificacion = models.CharField(max_length=100,null=True, blank=True)
    rampa_de_acceso = models.BooleanField(default=False, null=True, blank=True)
    ruta_de_evacuacion = models.BooleanField(default=False, null=True, blank=True)
    sanitario_para_personas_con_discapacidad = models.BooleanField(default=False, null=True, blank=True)
    


# Seccion Ubicacion

class ColindanciasIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='colindancias')
    ORIENTACION_CHOICES = [
        ('SIN INFORMACIÓN', 'SIN INFORMACIÓN'),
        ('NORTE', 'NORTE'),
        ('SUR', 'SUR'),
        ('ESTE', 'ESTE'),
        ('OESTE', 'OESTE'),
        ('NORESTE', 'NORESTE'),
        ('NOROESTE', 'NOROESTE'),
        ('SURESTE', 'SURESTE'),
        ('SUROESTE', 'SUROESTE'),
        ('PONIENTE', 'PONIENTE'),
        ('ORIENTE', 'ORIENTE')
    ]
    orientacion = models.CharField(max_length=15,choices=ORIENTACION_CHOICES, null=False, blank=True)
    colindancia = models.CharField(max_length=100, null=True, blank=True)
    medida_en_metros = models.CharField(max_length=100, null=True, blank=True)

# ----------------



# Titulo de Propiedad
class DocumentoPropiedadIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='docprop')
    fecha_creacion_DOC = models.DateField(null=False)
    archivo = models.FileField(upload_to='documentos_propiedad/', blank=True, null=True, editable=True)
    propietario_inmueble_choice = [
            ("SIN INFORMACIÓN", "SIN INFORMACIÓN"),
            ("ENTIDAD PARAESTATAL", "ENTIDAD PARAESTATAL"),
            ("GOBIERNO FEDERAL", "GOBIERNO FEDERAL"),
            ("ORGANISMO DESCENTRALIZADO NO SECTORIZADOS", "ORGANISMO DESCENTRALIZADO NO SECTORIZADOS"),
            ("PODER LEGISLATIVO", "PODER LEGISLATIVO"),
            ("PODER JUDICIAL", "PODER JUDICIAL"),
            ("INSTITUCIÓN AUTÓNOMA", "INSTITUCIÓN AUTÓNOMA"),
            ("ÓRGANO DESCONCENTRADO", "ÓRGANO DESCONCENTRADO"),
            ("OTROS", "OTROS"),
        ]
    propietario_inmueble =  models.CharField(max_length=100, choices=propietario_inmueble_choice, default="SIN INFORMACIÓN")

    institucion_propietario = models.CharField(max_length=100)
    SUPERFICIE_CHOICES = [
        ('SIN INFORMACIÓN', 'SIN INFORMACIÓN'),
        ('Escritura Pública', 'Escritura Pública'),
        ('Contrato', 'Contrato'),
        ('Acta o Resolución de Adjudicación', 'Acta o Resolución de Adjudicación'),
        ('Convenio de Cesión', 'Convenio de Cesión'),
        ('Decreto de Expropiación', 'Decreto de Expropiación'),
        ('Resolución Judicial', 'Resolución Judicial'),
        ('Resolución Administrativa', 'Resolución Administrativa'),
        ('Inmatriculación Administrativa', 'Inmatriculación Administrativa'),
        ('Declaratoria de Nacionalización', 'Declaratoria de Nacionalización'),
        ('Acuerdo Ministerial de Aseguramiento de Bienes', 'Acuerdo Ministerial de Aseguramiento de Bienes'),
        ('Ley o Decreto Constitutivo de una Institución Pública', 'Ley o Decreto Constitutivo de una Institución Pública'),
        ('Contrato o Aportación a un Fideicomiso', 'Contrato o Aportación a un Fideicomiso'),
        ('Título de Propiedad', 'Título de Propiedad'),
        ('Resolución Presidencial Agraria', 'Resolución Presidencial Agraria'),
        ('Declaratoria de Propiedad Federal', 'Declaratoria de Propiedad Federal'),
        ('Dación en Pago', 'Dación en Pago'),
        ('Información Ad Perpetuam', 'Información Ad Perpetuam'),
    ]
    
    superficie_amparada_m2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_documento = models.CharField(max_length=100, choices=SUPERFICIE_CHOICES, default='SIN INFORMACIÓN')
    numero_de_documento = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    expedido_por = models.CharField(max_length=100)
    INSCRIPCION_RPPF_CHOICES = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    
    inscripcion_rppf = models.CharField(max_length=2, choices=INSCRIPCION_RPPF_CHOICES, default='No')
    folio_real_federal = models.CharField(max_length=50, null=True, blank=True)
    fecha_inscripcion_federal = models.DateField(null=True, blank=True)
    
    INSCRIPCION_REGISTRO_LOCAL_CHOICES = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    
    inscripcion_registro_local = models.CharField(max_length=2, choices=INSCRIPCION_REGISTRO_LOCAL_CHOICES, default='No')
    folio_real_local = models.CharField(max_length=50, null=True, blank=True)
    folio_real_auxiliar = models.CharField(max_length=50, null=True, blank=True)
    nombre_libro = models.CharField(max_length=100, null=True, blank=True)
    tomo_o_volumen = models.CharField(max_length=50, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    foja_o_folio = models.CharField(max_length=50, null=True, blank=True)
    seccion = models.CharField(max_length=50, null=True, blank=True)
    fecha_inscripcion_local = models.DateField(null=True, blank=True)

    

#--------------------------- Valor (datos de los Avalúos de Otras Instituciones)---------------------------
class DatosAvaluosIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='avaluos')
    numero_de_avaluo = models.CharField(max_length=255)
    valor_de_avaluo = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_valor_de_avaluo = models.DateField()
    uso_del_avaluo = models.CharField(max_length=255)
    valor_de_terreno = models.DecimalField(max_digits=12, decimal_places=2)
    valor_de_construccion = models.DecimalField(max_digits=12, decimal_places=2)

class OcupacionesIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='ocupaciones')
    OPCIONES_TIPO_PROCEDIMIENTO = [
        ('sin_informacion', 'SIN INFORMACIÓN'),
        ('administrativo', 'ADMINISTRATIVO'),
        ('averiguacion_previa', 'AVERIGUACIÓN PREVIA'),
        ('judicial', 'JUDICIAL'),
    ]

    OPCIONES_ESTATUS_PROCEDIMIENTO = [
        ('sin_informacion', 'SIN INFORMACIÓN'),
        ('activo', 'ACTIVO'),
        ('concluido', 'CONCLUIDO'),
    ]

    tipo_procedimiento = models.CharField(
        max_length=20,
        choices=OPCIONES_TIPO_PROCEDIMIENTO,
        default='sin_informacion'
    )

    nombre_ocupante = models.CharField(max_length=100)
    superficie_invadida = models.DecimalField(max_digits=10, decimal_places=2)
    no_expediente = models.CharField(max_length=50, null=True, blank=True)
    juzgado = models.CharField(max_length=50, null=True, blank=True)
    estatus_procedimiento = models.CharField(max_length=20, choices=OPCIONES_ESTATUS_PROCEDIMIENTO, default='sin_informacion',null=True)
    suspension_acto = models.CharField(
        max_length=3,
        choices=[("Si", "Sí"), ("No", "No")],
        default="No",
        null=True
    )

    recuperado = models.CharField(
        max_length=3,
        choices=[("Si", "Sí"), ("No", "No")],
        default="No",
        null=True
    )
    fecha_recuperado = models.DateField(null=True, blank=True)
    
    
class TramitesDisposicionIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='dispocisiones')
    tramite_disposicion_choices = [
        ('SIN INFORMACIÓN', 'Sin Información'),
        ('ACUERDO DE DESINCORPORACIÓN', 'Acuerdo de Desincorporación'),
        ('ACUERDO DE DESTINO', 'Acuerdo de Destino'),
        ('ACUERDO INCORPORACIÓN', 'Acuerdo de Incorporación'),
        ('ARRENDAMIENTO', 'Arrendamiento'),
        ('COMERCIALIZACIÓN', 'Comercialización'),
        ('COMODATO', 'Comodato'),
        ('CONCESIÓN', 'Concesión'),
        ('DONACIÓN', 'Donación'),
        ('EMISIÓN DE DECLARATORIA DE PROPIEDAD FEDERAL', 'Emisión de Declaratoria de Propiedad Federal'),
        ('EXPEDICIÓN DE CERTIFICADO DE USO', 'Expedición de Certificado de Uso'),
        ('PERMISO', 'Permiso'),
        ('PUESTA A DISPOSICIÓN', 'Puesta a Disposición'),
        ('VENTA DE INMUEBLES EN FORMA DIRECTA', 'Venta de Inmuebles en Forma Directa'),
    ]

    tramite_disposicion = models.CharField(max_length=50, choices=tramite_disposicion_choices, null=False, blank=True)
    estatus_choices = [
        ('SIN INFORMACIÓN', 'Sin Información'),
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    estatus = models.CharField(max_length=20, choices=estatus_choices, default='SIN INFORMACIÓN')
    numero_de_expediente = models.CharField(max_length=50, null=True, blank=True)

class Documento_ocupacionIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='docOcupacion')
    TIPO_DOCUMENTO_CHOICES = (
    ('SIN INFORMACIÓN', 'SIN INFORMACIÓN'),
    ('ACTA DE ASAMBLEA EJIDATARIOS', 'ACTA DE ASAMBLEA EJIDATARIOS'),
    ('ACTA DE ENTREGA DE ESPACIOS EN INMUEBLES FEDERALES COMPARTIDOS', 'ACTA DE ENTREGA DE ESPACIOS EN INMUEBLES FEDERALES COMPARTIDOS'),
    ('ACTA DE ENTREGA DE OBRA', 'ACTA DE ENTREGA DE OBRA'),
    ('ACTA DE ENTREGA RECEPCIÓN', 'ACTA DE ENTREGA RECEPCIÓN'),
    ('ACTA DE OCUPACIÓN ADMINISTRATIVA', 'ACTA DE OCUPACIÓN ADMINISTRATIVA'),
    ('ACUERDO DE DESTINO', 'ACUERDO DE DESTINO'),
    ('ADQUISIONES POSTERIORES A 1004', 'ADQUISIONES POSTERIORES A 1004'),
    ('ARRENDAMIENTO', 'ARRENDAMIENTO'),
    ('ART. 59 FR. VI LGBN (ACTOS JURÍDICOS QUE INTERVIENE SFP)', 'ART. 59 FR. VI LGBN (ACTOS JURÍDICOS QUE INTERVIENE SFP)'),
    ('CERTIFICADO DE ASIGNACIÓN DE ESPACIOS EN INMUEBLES FEDERALES COMPARTIDOS', 'CERTIFICADO DE ASIGNACIÓN DE ESPACIOS EN INMUEBLES FEDERALES COMPARTIDOSCERTIFICADO DE ASIGNACIÓN DE ESPACIOS EN INMUEBLES FEDERALES COMPARTIDOS'),
    ('CERTIFICADO DE DERECHO DE USO', 'CERTIFICADO DE DERECHO DE USO'),
    ('COMODATO', 'COMODATO'),
    ('CONCESIÓN', 'CONCESIÓN'),
    ('CONVENIO', 'CONVENIO'),
    ('DECLARATORIA DE SUJECIÓN AL RÉGIMEN DE DOMINIO PÚBLICO', 'DECLARATORIA DE SUJECIÓN AL RÉGIMEN DE DOMINIO PÚBLICO'),
    ('DECLARATORIAS DE ACUERDO AL ART. 55 LGBN', 'DECLARATORIAS DE ACUERDO AL ART. 55 LGBN'),
    ('DECRETO DE DESTINO', 'DECRETO DE DESTINO'),
    ('DECRETO DE EXPROPIACIÓN', 'DECRETO DE EXPROPIACIÓN'),
    ('DEPÓSITO', 'DEPÓSITO'),
    ('DESTINO DE HECHO', 'DESTINO DE HECHO'),
    ('DOCUMENTO DE ASIGNACIÓN DE ESPACIOS', 'DOCUMENTO DE ASIGNACIÓN DE ESPACIOS'),
    ('NO APLICA', 'NO APLICA'),
    ('OTROS', 'OTROS'),
    )
    tipo_de_documento = models.CharField(max_length=150, choices=TIPO_DOCUMENTO_CHOICES)
    fecha_documento = models.DateField()
    
    INSCRIPCION_RPPF_CHOICES = (
        ('Si', 'Si'),
        ('No', 'No'),
    )
    inscripcion_RPPF = models.CharField(max_length=2, choices=INSCRIPCION_RPPF_CHOICES, default='No')
    folio_real_federal = models.CharField(max_length=255, null=True, blank=True)
    fecha_inscripcion_federal = models.DateField(null=True, blank=True)
    
class InstitucionesOcupantesIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='instOcupante')
    institucion_publica_ocupante = models.CharField(max_length=150, null=True, blank=True)
    superficie_asignada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)
    uso_institucion_ocupante = models.CharField(max_length=150, null=True, blank=False)
    superficie_disponible = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)
    
class DatosTercerosIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='datosTerceros')
    TIPO_USUARIO_CHOICES = (
        ('SIN INFORMACIÓN', 'SIN INFORMACIÓN'),
        ('ARRENDAMIENTO', 'ARRENDAMIENTO'),
        ('ASIGNACIÓN', 'ASIGNACIÓN'),
        ('AUTORIZACIÓN', 'AUTORIZACIÓN'),
        ('COMODATO', 'COMODATO'),
        ('CONCESIÓN', 'CONCESIÓN'),
        ('CONVENIO', 'CONVENIO'),
        ('USUFRUCTO', 'USUFRUCTO'),
    )
    tipo_usuario_tercero = models.CharField(max_length=50, choices=TIPO_USUARIO_CHOICES,default='SIN INFORMACIÓN')
    BENEFICIARIO_CHOICES = (
        ('SIN INFORMACIÓN', 'SIN INFORMACIÓN'),
        ('ASOCIACIÓN CIVIL', 'ASOCIACIÓN CIVIL'),
        ('ORGANISMO INTERNACIONAL', 'ORGANISMO INTERNACIONAL'),
        ('PERSONA FÍSICA', 'PERSONA FÍSICA'),
        ('PERSONA MORAL', 'PERSONA MORAL'),
    )

    beneficiario = models.CharField(max_length=50, choices=BENEFICIARIO_CHOICES, default='SIN INFORMACIÓN')
    nombre_beneficiario = models.CharField(max_length=255)
    rfc = models.CharField( max_length=13)
    fecha_inicio_vigencia = models.DateField(null=True, blank=True)
    fecha_termino_vigencia = models.DateField(null=True, blank=True)
    prorroga = models.DateField(null=True, blank=True)
    inscripcion_folio_real_federal = models.CharField(max_length=255,null=True, blank=True)
    superficie_objeto_ocupacion_metros = models.DecimalField(max_digits=10,decimal_places=2,null=True , blank=True)
    uso = models.CharField( max_length=255,null=True, blank=True )
    
    
    
    
class MensajeIMP(models.Model):
    task = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='mensajes',verbose_name="Inmueble")
    asunto = models.CharField(max_length=100, null=True)
    mensaje = models.TextField(null=True)
    enviar_a_imp = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Destino", related_name='mensajes_enviados_imp')
    enviado_por_imp = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Enviado", related_name='mensajes_recibidos_imp')
    fecha_envio = models.DateTimeField(auto_now_add=True)
    ESTADO_CHOICES = [
        ('Completado', 'Completado'),
        ('En Revisión', 'En Revision'),
        ('No Completado', 'No Completado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='No Completado')
    enlace = models.CharField(max_length=100, null=True, blank=True)