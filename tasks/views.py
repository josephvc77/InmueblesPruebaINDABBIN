
import os
from unittest import loader
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import View

from djangocrud import settings

from .forms import CreateDatosLlamadasForm, DictamenEstructuralIMPForm, DocumentoPropiedadIMPForm, Expedientes_CEDOCIMPForm, FoliosRealesIMPForm, NumeroPlanoIMPForm, ObservacionesForm, UserCreateForm
from .models import ColindanciasIMP, DatosAvaluosIMP, DatosLlamadasInmuebles, DatosTercerosIMP, DictamenEstructuralIMP, Documento_ocupacionIMP, DocumentoPropiedadIMP, EdificacionIMP, EdificioVerdeIMP, Expedientes_CEDOCIMP, FoliosRealesIMP, Inmueble, InstitucionesOcupantesIMP, MensajeIMP, NumeroPlanoIMP, OcupacionesIMP, RegistroLlamadas, TramitesDisposicionIMP

from .forms import TaskCreateForm


# Vista para cerrar sesión automáticamente
from django.contrib.auth import logout



from django.shortcuts import render

def permission_denied(request):
    return render(request, '403.html')


def error_404(request, exception):
    template_404 = '404.html'
    return render(request, template_404, status=404)

# myapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import CustomUserForm


@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'Adm_Users/user_list.html', {'users': users})

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import UserEditForm

@login_required
def edit_user(request, id):
    user = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Guarda el usuario y los grupos seleccionados
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('user_list')  # Cambia 'user_list' al nombre de tu vista de lista de usuarios
    else:
        form = UserEditForm(instance=user)

        mensajes = MensajeIMP.objects.filter(
            Q(enviar_a_imp=request.user) | Q(enviado_por_imp=request.user)
        ).order_by("-fecha_envio")

    return render(request, 'Adm_Users/edit_user.html', {'form': form, 'mensajes': mensajes})



@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('user_list')  # Cambia 'login' si tu URL tiene otro nombre
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = UserCreateForm()

    mensajes = MensajeIMP.objects.filter(
        Q(enviar_a_imp=request.user) | Q(enviado_por_imp=request.user)
    ).order_by("-fecha_envio")

    return render(request, 'Adm_Users/add_user.html', {'form': form, 'mensajes': mensajes})

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})
    


from django.contrib.auth.decorators import login_required


from django.contrib import messages

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # Mensaje con etiqueta específica
            messages.add_message(request, messages.ERROR, 'Usuario o contraseña incorrectos.', extra_tags='login-error')
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
            })
        else:
            messages.success(request, 'Inicio de sesión exitoso.')
            login(request, user)
            return redirect('principal')




@login_required
def signout(request):
    logout(request)
    messages.success(request, 'Sesión cerrada con éxito.')
    return redirect('/')

    
from django.http import JsonResponse
from datetime import date, datetime, time
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render
from .models import Inmueble

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from .models import Inmueble
from urllib.parse import urlencode
from django.http import HttpResponse

from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.utils import timezone


@login_required
@permission_required('tasks.add_tasks_inmueble', raise_exception=True)
def Inmuebles(request):
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')
    ur = request.GET.get('ur', '')
    orden = request.GET.get('ordenar', '')

    request.session['search_query'] = search_query
    request.session['prioridad'] = prioridad
    request.session['ur'] = ur
    request.session['ordenar'] = orden

    mensajes = MensajeIMP.objects.filter(
        Q(enviar_a_imp=request.user) | Q(enviado_por_imp=request.user)
    ).order_by("-fecha_envio")

    # Obtener los valores de búsqueda y filtros de la sesión
    search_query = request.session.get('search_query', '')
    prioridad = request.session.get('prioridad', '')
    ur = request.session.get('ur', '')

    inmuebles_list = Inmueble.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        datecompleted__isnull=True,
        estado='Activo'  # Filtra las tareas en estado 'Activo'
    )

    if prioridad:
        inmuebles_list = inmuebles_list.filter(prioridad=prioridad)

    if ur:
        inmuebles_list = inmuebles_list.filter(UR=ur)

    # Aplicar filtros de orden
    if orden == 'az':
        inmuebles_list = inmuebles_list.order_by('NombreInmueble')
    elif orden == 'za':
        inmuebles_list = inmuebles_list.order_by('-NombreInmueble')
    elif orden == 'nuevo':
        inmuebles_list = inmuebles_list.order_by('-updated')  # Más nuevo por fecha de actualización
    elif orden == 'viejo':
        inmuebles_list = inmuebles_list.order_by('creado')  # Más viejo por fecha de creación
    elif orden == 'utilizados':  # Suponiendo que 'utilizados' es un campo que indica la cantidad de usos
        inmuebles_list = inmuebles_list.order_by('-usos')  # Ordenar por el campo que cuenta usos (ajusta el campo según tu modelo)

    paginator = Paginator(inmuebles_list, 20)  # Muestra 20 inmuebles por página

    page = request.GET.get('page')
    inmuebles = paginator.get_page(page)



    total_pending_inmuebles = Inmueble.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        datecompleted__isnull=True
    ).count()  # Total de inmuebles pendientes por completar

    total_completed_inmuebles = Inmueble.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        datecompleted__isnull=False
    ).count()  # Total de inmuebles completados

    return render(request, 'importados.html', {
        'inmuebles': inmuebles, 
        'search_query': search_query,
        'total_pending_inmuebles': total_pending_inmuebles,
        'total_completed_inmuebles': total_completed_inmuebles,
        'mensajes': mensajes, 
        'prioridad': prioridad,
        'ur': ur,

        'orden': orden,
    })



from django.db.models import Q

@login_required
@permission_required('tasks.add_tasks_inmueble', raise_exception=True)
def principal(request):
    mensajes = MensajeIMP.objects.filter(
        Q(enviar_a_imp=request.user) | Q(enviado_por_imp=request.user)
    ).order_by("-fecha_envio")

    return render(request, 'home.html', {
        'mensajes': mensajes,
    })


    
@login_required
def completar_mensajeIMP(request, mensaje_id):
    if request.method == 'POST':
        mensaje = MensajeIMP.objects.get(id=mensaje_id)
        mensaje.estado = 'completado'
        mensaje.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})



@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
from django.http import JsonResponse
import csv

# Obtener entidades federativas desde un archivo CSV
def get_entidades_federativas(request):
    csv_path = os.path.join(os.path.dirname(__file__), 'data/mx.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        entidades_federativas = list(set(row['entidad_federativa'] for row in reader))

    return JsonResponse({'entidades_federativas': entidades_federativas})


# Obtener municipios por entidad federativa desde un archivo CSV
def get_municipios_by_entidad_federativa(request, entidad_federativa):
    csv_path = os.path.join(os.path.dirname(__file__), 'data/mx.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        municipios = [row['municipio_alcaldia'] for row in reader if row['entidad_federativa'] == entidad_federativa]

    return JsonResponse({'municipios': municipios})
    
import csv
import os
from django.http import JsonResponse

# Función para obtener la información de las salas desde un archivo CSV
def get_salas(request):
    csv_path = os.path.join(os.path.dirname(__file__), 'data/salas.csv')  # Ruta al archivo CSV
    salas_data = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            salas_data.append({
                'Nom_sala': row['Nom_sala'],
                'capacidad': row['capacidad'],
                'nivel': row['nivel'],
                'sala': row['sala']
            })

    return JsonResponse({'salas': salas_data})


@login_required
@permission_required('tasks.add_inmueble', raise_exception=True)
def crear_inmueble(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.user = request.user
            inmueble.creado = timezone.now()
            inmueble.save()
            messages.success(request, 'El inmueble se creó correctamente ✅')
            return redirect('inmuebles_list')
        else:
            messages.error(request, 'Hubo un error al crear el inmueble ❌')
    else:
        form = TaskCreateForm(user=request.user)
    
    return render(request, 'Inmuebles/crear_inmueble.html', {'form': form})



from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from PIL import Image as PILImage
import os
from django.contrib.auth.decorators import login_required

@login_required
def generate_pdfIMP(request, task_id):
    # Buscar el inmueble por ID
    inmueble = get_object_or_404(Inmueble, id=task_id)

    # Crear la respuesta HTTP para el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_inmueble_{inmueble.rfi}.pdf"'

    # Crear el PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Agregar una imagen al inicio (puedes cambiar la ruta)
    # image_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'logosep.webp')
    # img = Image(image_path, width=150, height=50)  # Ajusta el tamaño de la imagen según sea necesario
    # elements.append(img)
    elements.append(Spacer(1, 12))  # Agrega un espacio después de la imagen
    

    # Encabezado
    elements.append(Paragraph("<b>Reporte de Inmueble</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Datos Generales
    elements.append(Paragraph("<b>Encabezado - Datos Generales</b>", styles['Heading2']))
    encabezado_data = [
        ["Campo", "Valor"],
        ["RFI", inmueble.rfi],
        ["Asignado a", inmueble.assigned_to],
        ["Fecha Límite", inmueble.deadline.strftime('%d/%m/%Y') if inmueble.deadline else "N/A"],
        ["Proveedor", inmueble.rfiProv],
        ["Nombre del Inmueble", inmueble.NombreInmueble],
        ["UR", inmueble.UR],
        ["Sección del Inventario", inmueble.seccion_del_inventario],
        ["Causa de Alta", inmueble.causa_alta],
        ["Prioridad", inmueble.prioridad],
        ["Sector", inmueble.Sector],
        ["Nombre de la Institución", inmueble.Nombre_de_la_institucion_que_administra_el_inmueble],
        ["Naturaleza Jurídica", inmueble.Naturaleza_Juridica_de_la_Institucion],
        ["Dependencia Administradora", inmueble.Dependencia_Administradora],
        ["Subsección", inmueble.subSeccion],
        ["Certificado de Seguridad", inmueble.certificado_de_seguridad],
        ["Sentido del Dictamen", inmueble.sentido_del_Dictamen],
        ["Descripción del Sentido del Dictamen", inmueble.descripcion_del_sentido_del_Dictamen],
        ["Fecha del Documento", inmueble.fecha_documento.strftime('%d/%m/%Y') if inmueble.fecha_documento else "N/A"],
        ["Subir Archivo", inmueble.subir_archivo],
        ["No. de Identificador Expediente I.", inmueble.no_de_identificador_del_expediente_institucion]
    ]
    elements.append(create_table(encabezado_data))
    elements.append(PageBreak())


   # Ubicación
    elements.append(Paragraph("<b>Ubicación</b>", styles['Heading2']))
    ubicacion_data = [
        ["Campo", "Valor"],
        ["País", inmueble.pais],
        ["Entidad Federativa", inmueble.entidad_federativa],
        ["Municipio/Alcaldía", inmueble.municipio_alcaldia],
        ["Municipio No Existente", inmueble.municipio_no_existente],
        ["Localidad", inmueble.localidad],
        ["Componente Espacial", inmueble.componente_espacial],
        ["Fotografía de la Ubicación", f'URL o Ruta: {inmueble.fotografia_de_la_ubicacion}'],  # Aquí asumo que es una URL o ruta
        ["Tipo de Vialidad", inmueble.tipo_vialidad],
        ["Nombre de Vialidad", inmueble.nombre_vialidad],
        ["Número Exterior", inmueble.numero_exterior],
        ["Número Exterior 2", inmueble.numero_exterior_2],
        ["Número Interior", inmueble.numero_interior],
        ["Tipo de Asentamiento", inmueble.tipo_asentamiento],
        ["Nombre de Asentamiento", inmueble.nombre_asentamiento],
        ["Código Postal", inmueble.codigo_postal],
        ["Entre Vialidades Referencia 1", inmueble.entre_vialidades_referencia1],
        ["Entre Vialidades Referencia 2", inmueble.entre_vialidades_referencia2],
        ["Vialidad Posterior", inmueble.vialidad_posterior],
        ["Descripción de la Ubicación", inmueble.descripcion_ubicacion],
        ["Datum", inmueble.datum],
        ["UTM X", inmueble.utmx],
        ["UTM Y", inmueble.utmy],
        ["UTM Zona", inmueble.utm_zona],
        ["Latitud", inmueble.latitud],
        ["Longitud", inmueble.longitud]
    ]
    elements.append(create_table(ubicacion_data))
    elements.append(PageBreak())

   # Características
    elements.append(Paragraph("<b>Características</b>", styles['Heading2']))
    caracteristicas_data = [
        ["Campo", "Valor"],
        ["Superficie del Terreno (M2)", inmueble.superficie_del_terreno_en_M2],
        ["Superficie del Terreno (HA)", inmueble.superficie_del_terreno_HA],
        ["Superficie de Desplante (M2)", inmueble.superficie_de_desplante_en_M2],
        ["Superficie Construida (M2)", inmueble.superficie_construida_en_M2],
        ["Superficie Útil (M2)", inmueble.superficie_util_m2],
        ["Zona de Ubicación", inmueble.zona_ubicacion],
        ["Tipo de Inmueble Rural", inmueble.tipo_inmueble_rural],
        ["Uso Dominante de la Zona", inmueble.uso_dominante_zona],
        ["Calidad de la Construcción", inmueble.calidad_construccion],
        ["Clasificación por Edad", inmueble.clasificacion_edad],
        ["Categoría", inmueble.categoria],
        ["Grado de Consolidación", inmueble.grado_consolidacion],
        ["Servicios", inmueble.servicios],
        ["Teléfono del Inmueble", inmueble.telefono_inmueble],
        ["Fecha de Inicio de Construcción", inmueble.fecha_inicio_construccion.strftime('%d/%m/%Y') if inmueble.fecha_inicio_construccion else "N/A"],
        ["Siglo de Construcción", inmueble.siglo_construccion],
        ["Fecha de Última Remodelación", inmueble.fecha_ultima_remodelacion.strftime('%d/%m/%Y') if inmueble.fecha_ultima_remodelacion else "N/A"],
        ["Monumento", "Sí" if inmueble.monumento else "No"],
        ["Histórico", "Sí" if inmueble.historico else "No"],
        ["Artístico", "Sí" if inmueble.artistico else "No"],
        ["Arqueológico", "Sí" if inmueble.arqueologico else "No"],
        ["Estado de Conservación", inmueble.estado_conservacion],
        ["Clave INAH", inmueble.clave_inah],
        ["Folio Real INAH", inmueble.folio_real_inah],
        ["No. Plano INAH", inmueble.no_plano_inah],
        ["Clave CNMH", inmueble.clave_cnmh],
        ["Clave DGSMPCCONACULTA", inmueble.clave_dgsmpc_conaculta],
        ["Fecha de Inscripción en la UNESCO", inmueble.fecha_inscripcion_unesco if inmueble.fecha_inscripcion_unesco else "N/A"],
        ["Observaciones Históricas", inmueble.observaciones_historicas]
    ]
    elements.append(create_table(caracteristicas_data))
    elements.append(Spacer(1, 12))  

    # Uso
    elements.append(Spacer(1, 12))  
    elements.append(Paragraph("<b>Uso</b>", styles['Heading2']))
    uso_data = [
        ["Campo", "Valor"],
        ["Usuario Principal del Inmueble", inmueble.usuario_principal_del_inmueble],
        ["Uso Genérico", inmueble.usoGenerico],
        ["Uso Específico", inmueble.usoEspecifico],
        ["Uso de Suelo Autorizado", inmueble.uso_de_suelo_autorizado],
        ["Número de Empleados en el Inmueble", inmueble.numero_de_empleados_en_el_inmueble],
        ["Documento que Autoriza Ocupación", inmueble.documento_que_autoriza_ocupacion],
        ["Número de Documentos de Ocupación", inmueble.numero_de_documentos_de_ocupacion],
        ["Instituciones Ocupantes", inmueble.instituciones_ocupantes],
        ["Usuarios de Terceros", inmueble.usuarios_terceros],
        ["Siglo o Periodo", inmueble.siglo_o_periodo],
        ["Correlativo", inmueble.correlativo],
        ["Conjunto", inmueble.conjunto],
        ["Clave INBAL", inmueble.clave_inbal],
        ["Registro Único INAH", inmueble.registro_unico_inah]
    ]
    elements.append(create_table(uso_data))
    elements.append(PageBreak())

    # Aprovechamiento
    elements.append(Paragraph("<b>Aprovechamiento</b>", styles['Heading2']))
    aprovechamiento_data = [
        ["Campo", "Valor"],
        ["Aprovechamiento", inmueble.aprovechamiento],
        ["Inmueble con Atención al Público", "Sí" if inmueble.inmueble_con_atencion_al_publico else "No"],
        ["Población Beneficiada", inmueble.poblacion_beneficiada],
        ["Población en Servicio", inmueble.poblacion_servicio],
        ["Cuenta con Proyecto de Uso Inmediato Desarrollado", "Sí" if inmueble.cuenta_con_proyecto_de_uso_inmediato_desarrollado else "No"],
        ["Inversión Requerida", inmueble.inversion_requerida],
        ["Fuente de Financiamiento", inmueble.fuente_financiamiento],
        ["Fecha Solicitud", inmueble.fecha_solicitud if inmueble.fecha_solicitud else "N/A"],
        ["Inmueble no Aprovechable (Especificar)", inmueble.inmueble_no_aprovechable_especificar],
        ["Gasto Anual de Mantenimiento", inmueble.gasto_anual_de_mantenimiento],
        ["Inmueble en Condominio", "Sí" if inmueble.inmueble_en_condominio else "No"],
        ["Superficie Total", inmueble.superficie_total],
        ["Indiviso", inmueble.indiviso]
    ]
    elements.append(create_table(aprovechamiento_data))
    elements.append(PageBreak())

    # Valor
    elements.append(Paragraph("<b>Valor</b>", styles['Heading2']))
    valor_data = [
        ["Campo", "Valor"],
        ["Valor Contable", inmueble.valor_contable],
        ["Fecha Valor Contable", inmueble.fecha_valor_contable if inmueble.fecha_valor_contable else "N/A"],
        ["Valor Asegurable", inmueble.valor_asegurable],
        ["Fecha Valor Asegurable", inmueble.fecha_valor_asegurable if inmueble.fecha_valor_asegurable else "N/A"],
        ["Valor Adquisición", inmueble.valor_adquisicion],
        ["Fecha Valor Adquisición", inmueble.fecha_valor_adquisicion if inmueble.fecha_valor_adquisicion else "N/A"],
        ["Valor Terreno", inmueble.valor_terreno],
        ["Valor Construcción", inmueble.valor_construccion],
        ["Valor Catastral Terreno", inmueble.valor_catastral_terreno],
        ["Valor Catastral Construcción", inmueble.valor_catastral_construccion],
        ["Valor Total Catastral", inmueble.valor_total_catastral],
        ["Fecha Valor Catastral", inmueble.fecha_valor_catastral if inmueble.fecha_valor_catastral else "N/A"],
        ["Documentación Soporte", inmueble.documentacion_soporte]
    ]
    elements.append(create_table(valor_data))
    elements.append(PageBreak())


    
    # Pie de Página
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<i>Este reporte fue generado por el SIISEP</i>", styles['Normal']))

    # Construcción del PDF
    pdf.build(elements)

    return response


def create_table(data):
    table = Table(data, colWidths=[180, 300])
    table.setStyle(TableStyle([  
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#691c32")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f9f9f9")),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10)
    ]))
    return table



import pandas as pd
from django.http import HttpResponse
from django.db.models import F



def export_tasks_to_excelIMP(request):
    # Obtener todas las tareas del usuario logueado
    inmueble = Inmueble.objects.filter()

    # Crear una lista vacía para almacenar los datos de tareas y modelos relacionados
    data = []

    # Recorrer todas las tareas y obtener los datos necesarios
    for task in inmueble:
        task_data = {
            'rfi': task.rfi,
            'rfiProv': task.rfiProv,
            'NombreInmueble': task.NombreInmueble,
            'seccion_del_inventario': task.seccion_del_inventario,
            'causa_alta': task.causa_alta,
            'prioridad': task.prioridad,
            'Sector': task.Sector,
            'Nombre_de_la_institucion_que_administra_el_inmueble': task.Nombre_de_la_institucion_que_administra_el_inmueble,
            'Naturaleza_Juridica_de_la_Institucion': task.Naturaleza_Juridica_de_la_Institucion,
            'Denominaciones_anteriores': task.Denominaciones_anteriores,
            'Dependencia_Administradora': task.Dependencia_Administradora,
            'subSeccion': task.subSeccion,
            'certificado_de_seguridad': task.certificado_de_seguridad,
            'sentido_del_Dictamen': task.sentido_del_Dictamen,
            'descripcion_del_sentido_del_Dictamen': task.descripcion_del_sentido_del_Dictamen,
            'fecha_documento': task.fecha_documento,
            'subir_archivo': task.subir_archivo,
            'no_de_identificador_del_expediente_institucion': task.no_de_identificador_del_expediente_institucion,
            # Ubicacion
            'pais': task.pais,
            'entidad_federativa': task.entidad_federativa,
            'municipio_alcaldia': task.municipio_alcaldia,
            'localidad': task.localidad,
            'componente_espacial': task.componente_espacial,
            'fotografia_de_la_ubicacion': task.fotografia_de_la_ubicacion,
            'tipo_vialidad': task.tipo_vialidad,
            'nombre_vialidad': task.nombre_vialidad,
            'numero_exterior': task.numero_exterior,
            'numero_exterior_2': task.numero_exterior_2,
            'numero_interior': task.numero_interior,
            'tipo_asentamiento': task.tipo_asentamiento,
            'nombre_asentamiento': task.nombre_asentamiento,
            'codigo_postal': task.codigo_postal,
            'entre_vialidades_referencia1': task.entre_vialidades_referencia1,
            'entre_vialidades_referencia2': task.entre_vialidades_referencia2,
            'vialidad_posterior': task.vialidad_posterior,
            'descripcion_ubicacion': task.descripcion_ubicacion,
            'datum': task.datum,
            'utmx': task.utmx,
            'utmy': task.utmy,
            'utm_zona': task.utm_zona,
            'latitud': task.latitud,
            'longitud': task.longitud,
            
            # Caracteristicas
            'superficie_del_terreno_en_M2': task.superficie_del_terreno_en_M2,
            'superficie_del_terreno_HA': task.superficie_del_terreno_HA,
            'superficie_de_desplante_en_M2': task.superficie_de_desplante_en_M2,
            'superficie_construida_en_M2': task.superficie_construida_en_M2,
            'superficie_util_m2': task.superficie_util_m2,
            'zona_ubicacion': task.zona_ubicacion,
            'tipo_inmueble_rural': task.tipo_inmueble_rural,
            'uso_dominante_zona': task.uso_dominante_zona,
            'calidad_construccion': task.calidad_construccion,
            'clasificacion_edad': task.clasificacion_edad,
            'categoria': task.categoria,
            'grado_consolidacion': task.grado_consolidacion,
            'servicios': task.servicios,
            'telefono_inmueble': task.telefono_inmueble,
            'fecha_inicio_construccion': task.fecha_inicio_construccion,
            'siglo_construccion': task.siglo_construccion,
            'fecha_ultima_remodelacion': task.fecha_ultima_remodelacion,
            'monumento': task.monumento,
            'historico': task.historico,
            'artistico': task.artistico,
            'arqueologico': task.arqueologico,
            'clave_inah': task.clave_inah,
            'folio_real_inah': task.folio_real_inah,
            'no_plano_inah': task.no_plano_inah,
            'clave_cnmh': task.clave_cnmh,
            'clave_dgsmpc_conaculta': task.clave_dgsmpc_conaculta,
            'fecha_inscripcion_unesco': task.fecha_inscripcion_unesco,
            'observaciones_historicas': task.observaciones_historicas,
            'siglo_o_periodo': task.siglo_o_periodo,
            'correlativo': task.correlativo,
            'conjunto': task.conjunto,
            'clave_inbal': task.clave_inbal,
            'registro_unico_inah': task.registro_unico_inah,
            'estado_conservacion': task.estado_conservacion,

            # Uso
            'usuario_principal_del_inmueble': task.usuario_principal_del_inmueble,
            'usoGenerico': task.usoGenerico,
            'usoEspecifico': task.usoEspecifico,
            'uso_de_suelo_autorizado': task.uso_de_suelo_autorizado,
            'numero_de_empleados_en_el_inmueble': task.numero_de_empleados_en_el_inmueble,
            'documento_que_autoriza_ocupacion': task.documento_que_autoriza_ocupacion,
            'numero_de_documentos_de_ocupacion': task.numero_de_documentos_de_ocupacion,
            'instituciones_ocupantes': task.instituciones_ocupantes,
            'usuarios_terceros': task.usuarios_terceros,
            # Aprovechamiento
            'aprovechamiento': task.aprovechamiento,
            'inmueble_con_atencion_al_publico': task.inmueble_con_atencion_al_publico,
            'poblacion_beneficiada': task.poblacion_beneficiada,
            'poblacion_servicio': task.poblacion_servicio,
            'cuenta_con_proyecto_de_uso_inmediato_desarrollado': task.cuenta_con_proyecto_de_uso_inmediato_desarrollado,
            'inversion_requerida': task.inversion_requerida,
            'fuente_financiamiento': task.fuente_financiamiento,
            'fecha_solicitud': task.fecha_solicitud,
            'inmueble_no_aprovechable_especificar': task.inmueble_no_aprovechable_especificar,
            'gasto_anual_de_mantenimiento': task.gasto_anual_de_mantenimiento,
            'inmueble_en_condominio': task.inmueble_en_condominio,
            'superficie_total': task.superficie_total,
            'indiviso': task.indiviso,

            # Valor
            'valor_contable': task.valor_contable,
            'fecha_valor_contable': task.fecha_valor_contable,
            'valor_asegurable': task.valor_asegurable,
            'fecha_valor_asegurable': task.fecha_valor_asegurable,
            'valor_adquisicion': task.valor_adquisicion,
            'fecha_valor_adquisicion': task.fecha_valor_adquisicion,
            'valor_terreno': task.valor_terreno,
            'valor_construccion': task.valor_construccion,
            'valor_catastral_terreno': task.valor_catastral_terreno,
            'valor_catastral_construccion': task.valor_catastral_construccion,
            'valor_total_catastral': task.valor_total_catastral,
            'fecha_valor_catastral': task.fecha_valor_catastral,
            'documentacion_soporte': task.documentacion_soporte,         
            # Agrega otros campos de tarea según sea necesario...

            
        }

        # Consulta para obtener la Edificacion relacionada con la tarea actual (si existe)
        edificaciones = EdificacionIMP.objects.filter(task=task)
        
        # Crear una lista para almacenar los datos de todas las edificaciones relacionadas
        edificaciones_data = []

        for edificacion in edificaciones:
            edificacion_data = {
                'tipo_de_inmueble': edificacion.tipo_de_inmueble,
                'nombre_edificacion': edificacion.nombre_edificacion,
                'propietario_de_la_edificacion': edificacion.propietario_de_la_edificacion,
                'niveles_por_edificio': edificacion.niveles_por_edificio,
                'superficie_construida_por_edificacion_m2': edificacion.superficie_construida_por_edificacion_m2,
                'fecha_construccion_por_edificacion': edificacion.fecha_construccion_por_edificacion,
                'caracteristicas_de_la_edificacion': edificacion.caracteristicas_de_la_edificacion,
                'usoEdificacion': edificacion.usoEdificacion,
                'calidadEdificacion': edificacion.calidadEdificacion,
                'cajones_de_estacionamiento_por_edificacion': edificacion.cajones_de_estacionamiento_por_edificacion,
                'rampa_de_acceso': edificacion.rampa_de_acceso,
                'ruta_de_evacuacion': edificacion.ruta_de_evacuacion,
                'sanitario_para_personas_con_discapacidad': edificacion.sanitario_para_personas_con_discapacidad,
            }

            edificaciones_data.append(edificacion_data)

        # Ahora, el 'task_data' incluirá la lista de edificaciones relacionadas
        task_data['edificaciones'] = edificaciones_data
        
         # Consulta para obtener todas las colindancias relacionadas con la tarea actual
        colindancias = ColindanciasIMP.objects.filter(task=task)
        
        colindancias_data = []

        for colindancia in colindancias:
            colindancia_data = {
                'orientacion': colindancia.orientacion,
                'colindancia': colindancia.colindancia,
                'medida_en_metros': colindancia.medida_en_metros,
            }

            colindancias_data.append(colindancia_data)

        # Ahora, el 'task_data' incluirá la lista de colindancias relacionadas
        task_data['colindancias'] = colindancias_data
        
    
        
        # DOCUMENTO DE OCUPACION-------------------------------------------------------
        documento_ocupacion = Documento_ocupacionIMP.objects.filter(task=task)
        documento_ocupacion_data = []
        for doc_ocupacion in documento_ocupacion:
            documento_de_ocupacion = {
                'tipo_de_documento': doc_ocupacion.tipo_de_documento,
                'fecha_documento': doc_ocupacion.fecha_documento,
                'inscripcion_RPPF': doc_ocupacion.inscripcion_RPPF,
                'folio_real_federal': doc_ocupacion.folio_real_federal,
                'fecha_inscripcion_federal': doc_ocupacion.fecha_inscripcion_federal
            }
            documento_ocupacion_data.append(documento_de_ocupacion)
        task_data['documento_ocupacion'] = documento_ocupacion_data
        
            # INSTITUCIONES OCUPANTES-------------------------------------------------------
        instituciones_ocupantes = InstitucionesOcupantesIMP.objects.filter(task=task)
        
        instituciones_ocupantes_data = []
        
        for inst_ocupante in instituciones_ocupantes:
            Instituciones_ocupantes = {
                'institucion_publica_ocupante': inst_ocupante.institucion_publica_ocupante,
                'superficie_asignada': inst_ocupante.superficie_asignada,
                'uso_institucion_ocupante': inst_ocupante.uso_institucion_ocupante,
                'superficie_disponible': inst_ocupante.superficie_disponible
            }
            instituciones_ocupantes_data.append(Instituciones_ocupantes)
        task_data['instituciones_ocupantes'] = instituciones_ocupantes_data
        
        
        # DATOS TERCEROS-------------------------------------------------------------
        dato_terceros = DatosTercerosIMP.objects.filter(task=task)
        datos_terceros_data = []
        for datos in dato_terceros:
            datos_terceros = {
                'tipo_usuario_tercero': datos.tipo_usuario_tercero,
                'beneficiario': datos.beneficiario,
                'nombre_beneficiario': datos.nombre_beneficiario,
                'rfc': datos.rfc,
                'fecha_inicio_vigencia': datos.fecha_inicio_vigencia,
                'fecha_termino_vigencia': datos.fecha_termino_vigencia,
                'prorroga': datos.prorroga,
                'inscripcion_folio_real_federal': datos.inscripcion_folio_real_federal,
                'superficie_objeto_ocupacion_metros': datos.superficie_objeto_ocupacion_metros,
                'uso': datos.uso
            }
            datos_terceros_data.append(datos_terceros)
        task_data['dato_terceros'] = datos_terceros_data
            
        
        # TRAMITE DE DISPOSICION--------------------------------------------------
        tramites_disposicion = TramitesDisposicionIMP.objects.filter(task=task)
        tramites_disposicion_data = []
        for tramite in tramites_disposicion:
            tramites_de_disposicion = {
                'tramite_disposicion': tramite.tramite_disposicion,
                'estatus': tramite.estatus,
                'numero_de_expediente': tramite.numero_de_expediente
            }
            tramites_disposicion_data.append(tramites_de_disposicion)
        task_data['tramites_disposicion'] = tramites_disposicion_data
        
        # OCUPACIONES-----------------------------------------------------------
        ocupaciones = OcupacionesIMP.objects.filter(task=task)
        ocupaciones_data = []
        for ocupacion in ocupaciones:
            ocupacion_data = {
                'tipo_procedimiento': ocupacion.tipo_procedimiento,
                'nombre_ocupante': ocupacion.nombre_ocupante,
                'superficie_invadida': ocupacion.superficie_invadida,
                'no_expediente': ocupacion.no_expediente,
                'juzgado': ocupacion.juzgado,
                'estatus_procedimiento': ocupacion.estatus_procedimiento,
                'suspension_acto': ocupacion.suspension_acto,
                'recuperado': ocupacion.recuperado,
                'fecha_recuperado': ocupacion.fecha_recuperado
            }
            ocupaciones_data.append(ocupacion_data)  
        task_data['ocupaciones'] = ocupaciones_data
        
        
        # DATOS AVALUOS----------------------------------------------------------
        datos_avaluos = DatosAvaluosIMP.objects.filter(task=task)
        datos_avaluos_data = []
        for dato_avaluo in datos_avaluos:
            datos_avaluo_data = {
                'numero_de_avaluo': dato_avaluo.numero_de_avaluo,
                'valor_de_avaluo': dato_avaluo.valor_de_avaluo,
                'fecha_valor_de_avaluo': dato_avaluo.fecha_valor_de_avaluo,
                'uso_del_avaluo': dato_avaluo.uso_del_avaluo,
                'valor_de_terreno': dato_avaluo.valor_de_terreno,
                'valor_de_construccion': dato_avaluo.valor_de_construccion
            }
            datos_avaluos_data.append(datos_avaluo_data)
        task_data['datos_avaluos'] = datos_avaluos_data
                
                
        # DOCUMENTOS DE PROPIEDAD------------------------------------------------- 
        doc_propiedads = DocumentoPropiedadIMP.objects.filter(task=task)
        doc_propiedads_data =[]
        for doc_propiedad in doc_propiedads:
            doc_propiedad_data = {
                'fecha_creacion_DOC': doc_propiedad.fecha_creacion_DOC,
                'archivo': doc_propiedad.archivo,
                'propietario_inmueble': doc_propiedad.propietario_inmueble,
                'institucion_propietario': doc_propiedad.institucion_propietario,
                'superficie_amparada_m2': doc_propiedad.superficie_amparada_m2,
                'tipo_documento': doc_propiedad.tipo_documento,
                'numero_de_documento': doc_propiedad.numero_de_documento,
                'expedido_por': doc_propiedad.expedido_por,
                'inscripcion_rppf': doc_propiedad.inscripcion_rppf,
                'folio_real_federal': doc_propiedad.folio_real_federal,
                'fecha_inscripcion_federal': doc_propiedad.fecha_inscripcion_federal,
                'inscripcion_registro_local': doc_propiedad.inscripcion_registro_local,
                'folio_real_local': doc_propiedad.folio_real_local,
                'folio_real_auxiliar': doc_propiedad.folio_real_auxiliar,
                'nombre_libro': doc_propiedad.nombre_libro,
                'tomo_o_volumen': doc_propiedad.tomo_o_volumen,
                'numero': doc_propiedad.numero,
                'foja_o_folio': doc_propiedad.foja_o_folio,
                'seccion': doc_propiedad.seccion,
                'fecha_inscripcion_local': doc_propiedad.fecha_inscripcion_local
            }
            doc_propiedads_data.append(doc_propiedad_data)
        task_data['doc_propiedads'] = doc_propiedads_data
        
        # Folios Reales
        folios_reales = FoliosRealesIMP.objects.filter(task=task)
        folios_reales_data = []  # Utiliza una lista para almacenar los datos de folios reales
        for folio_real in folios_reales:
            folio_real_data = {
                'Folio': folio_real.folios_reales_data
            }
            folios_reales_data.append(folio_real_data)  # Agrega cada diccionario a la lista
        task_data['folios_reales'] = folios_reales_data  # Asigna la lista de datos a 'folios_reales' en task_data

        
        
        # # Obtener datos de FoliosReales relacionados con la tarea
        # folios_reales_data = task.foliosreales_set.values_list('folios_reales_data', flat=True)

        # # Obtener datos de NumeroPlano relacionados con la tarea
        # numero_plano_data = task.numeros_planos.values_list('numero_plano_data', flat=True)

        # # Obtener datos de Expedientes_CEDOC relacionados con la tarea
        # expedientes_cedoc_data = task.expedientes_cedoc_set.values_list('expediente_cedoc_data', flat=True)

        # edificio_verde_data = task.edificio_verde_set.values_list('edificio_verde_data', flat=True)

        # Combinar todos los datos en un solo diccionario
        # task_data.update({
            # 'folios_reales': ', '.join(folios_reales_data),
            # 'numero_plano': ', '.join(numero_plano_data),
            # 'expedientes_cedoc': ', '.join(expedientes_cedoc_data),
            # 'edificio_verde': ', '.join(edificio_verde_data)
        # })

        data.append(task_data)

    # Convertir la lista de datos a un DataFrame de Pandas
    df = pd.DataFrame(data)

    # Crear la respuesta del archivo Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="InmueblesImportados.xlsx"'

    # Escribir el DataFrame en el archivo Excel
    df.to_excel(response, index=False, engine='openpyxl')

    return response

import pandas as pd

excel_file = os.path.join(os.path.dirname(__file__), 'data/prueba1.xlsx')
csv_file = os.path.join(os.path.dirname(__file__), 'data/inmueblePrueba1.csv')

# Lee el archivo Excel
df = pd.read_excel(excel_file)

# Guarda los datos en un archivo CSV
df.to_csv(csv_file, index=False)



from tasks.resource import InmuebleResource, LlamadaResource
from tablib import Dataset 
from django.http import HttpResponse
from django.shortcuts import render
from tablib import Dataset


from tablib import Dataset
from django.contrib import messages
from django.http import HttpResponseForbidden

def staff_or_superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return HttpResponseForbidden("No tienes permisos para acceder a esta vista.")
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@staff_or_superuser_required
@permission_required('tasks.add_tasks_inmueble', raise_exception=True)
def importar(request):
    mensajes = MensajeIMP.objects.filter(
        Q(enviar_a_imp=request.user) | Q(enviado_por_imp=request.user)
    ).order_by("-fecha_envio")
    errores = []
    if request.method == 'POST':
        inmueble_resource = InmuebleResource()
        dataset = Dataset()
        
        archivo = request.FILES['archivo']

        if archivo.name.endswith(('xls', 'xlsx')):
            imported_data = dataset.load(archivo.read(), format='xlsx')
        else:
            messages.error(request, 'El archivo debe ser un Excel válido (.xls o .xlsx).')
            return render(request, 'importar.html')

        result = inmueble_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            # Importación real
            result = inmueble_resource.import_data(dataset, dry_run=False)
            messages.success(request, 'Los datos se importaron con éxito.')
        else:
            messages.error(request, 'Se encontraron errores en la importación.')
            for error in result.row_errors():
                row_index, row_errors = error
                errores.append(f"Fila {row_index + 1}: {', '.join([str(e.error) for e in row_errors])}")

    return render(request, 'importar.html', {"errores": errores, "mensajes": mensajes})


from tablib import Dataset
from django.contrib import messages
@login_required
def importar_Llamadas(request):
    if request.method == 'POST':
        inmueble_resource = LlamadaResource()
        dataset = Dataset()
        
        archivo = request.FILES['archivo']

        if archivo.name.endswith('.csv'):
            imported_data = dataset.load(archivo.read().decode('utf-8'), format='csv')
        elif archivo.name.endswith(('xls', 'xlsx')):
            imported_data = dataset.load(archivo.read(), format='xlsx')
        else:
            messages.error(request, 'El archivo no es ni un archivo CSV ni un archivo Excel válido.')
            return render(request, 'importarLlamadas.html')

        result = inmueble_resource.import_data(dataset, dry_run=True)
        
        if not result.has_errors():
            # Realiza la importación real
            result = inmueble_resource.import_data(dataset, dry_run=False)
            messages.success(request, 'Los datos se importaron con éxito.')
        else:
            messages.error(request, 'Se encontraron errores en la importación.')

    return render(request, 'importarLlamadas.html')



# Email 

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings

def contacto(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        # Renderizar el template del correo con los datos del formulario
        template = render_to_string('extends_importados/email_template.html', {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        })

        # Crear el objeto EmailMessage
        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,  # Remitente
            ['soporte.sii.sep@nube.sep.gob.mx']  # Destinatario(s)
        )

        # Configurar para que falle explícitamente si hay errores
        email.fail_silently = False

        # Enviar el correo
        email.send()

        # Mostrar un mensaje de éxito
        messages.success(request, 'Se ha enviado tu correo.')

        # Redirigir a alguna página después de enviar el correo
        return redirect('Inmuebles')  # Puedes cambiar 'Inmuebles' por la vista a la que quieres redirigir

    # Si el método de solicitud no es POST, renderizar la página de contacto
    return render(request, 'extends_importados/email.html')


@login_required
def create_DatosLlamadasInmueble(request):
    if request.method == 'POST':
        form = CreateDatosLlamadasForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            assigned_to = form.cleaned_data.get('assigned_to')
            if assigned_to:
                task.assigned_to = assigned_to
                task.user = assigned_to
            else:
                task.user = request.user
            task.save()
            return redirect('llamadas_inmuebles')
    else:
        form = CreateDatosLlamadasForm(user=request.user)
        mensajes = MensajeIMP.objects.filter(
        Q(enviar_a_imp=request.user) | Q(enviado_por_imp=request.user)
    ).order_by("-fecha_envio")
    context = {'form': form, 'mensajes': mensajes}
    return render(request, 'create_llamada.html', context)


@login_required
@permission_required('tasks.add_tasks_inmueble', raise_exception=True)
def llamadas_inmuebles(request):
    mensajes = MensajeIMP.objects.filter(
        Q(enviar_a_imp=request.user) | Q(enviado_por_imp=request.user)
    ).order_by("-fecha_envio")
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')
    ur = request.GET.get('ur', '')
    orden = request.GET.get('ordenar', '')

    # Filtrado inicial
    llamadas_list = DatosLlamadasInmuebles.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query),
        estado='Activo'
    )

    if prioridad:
        llamadas_list = llamadas_list.filter(prioridad=prioridad)
        
    if ur:
        llamadas_list = llamadas_list.filter(ur=ur)

    # Ordenación
    if orden == 'az':
        llamadas_list = llamadas_list.order_by('NombreInmueble')
    elif orden == 'za':
        llamadas_list = llamadas_list.order_by('-NombreInmueble')
    elif orden == 'nuevo':
        llamadas_list = llamadas_list.order_by('-updated')
    elif orden == 'viejo':
        llamadas_list = llamadas_list.order_by('creado')
    else:
        # Orden por defecto: más recientes primero
        llamadas_list = llamadas_list.order_by('-updated')

    # Paginación
    paginator = Paginator(llamadas_list, 20)
    page = request.GET.get('page')
    try:
        llamadas = paginator.page(page)
    except PageNotAnInteger:
        llamadas = paginator.page(1)
    except EmptyPage:
        llamadas = paginator.page(paginator.num_pages)

    total_pending_inmuebles = DatosLlamadasInmuebles.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query),
        estado='Activo'
    ).count()

    total_completed_inmuebles = DatosLlamadasInmuebles.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query),
        estado='Completado'
    ).count()
    
    ur_opciones = "CGEE,DGB,DGBTEPD,DGCFT,DGETAyCM,DGETI,DGRMyS,RESEMS".split(',')


    return render(request, 'llamadas.html', {
        'llamadas': llamadas, 
        'search_query': search_query,
        'total_pending_inmuebles': total_pending_inmuebles,
        'total_completed_inmuebles': total_completed_inmuebles,
        'prioridad': prioridad,
        'ur': ur,
        'orden': orden,
        'ur_opciones': ur_opciones,
        'mensajes': mensajes,
    })
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

from .models import DatosLlamadasInmuebles, RegistroLlamadas, MensajeIMP






def verificar_num_llamada(request):
    num_llamada = request.GET.get('num_llamada')
    ficha_id = request.GET.get('ficha_id')
    exists = RegistroLlamadas.objects.filter(NumLlamada=num_llamada, ficha_id=ficha_id).exists()
    return JsonResponse({'exists': exists})

import pandas as pd
from datetime import datetime, date, time
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import NamedStyle
from .models import DatosLlamadasInmuebles, RegistroLlamadas

@login_required
@permission_required('tasks.add_tasks_inmueble', raise_exception=True)
def export_Llamadas_to_excelIMP(request):
    # Obtener todas las tareas
    RLlamadas = DatosLlamadasInmuebles.objects.all()

    # Lista para almacenar los datos
    data = []

    for tarea in RLlamadas:
        task_data = {
            'RFI': tarea.rfi,
            'Nombre del Inmueble': tarea.NombreInmueble,
            'Estado': tarea.estado,
            'Prioridad': tarea.prioridad,
            'Tarea asignada': str(tarea.assigned_task) if tarea.assigned_task else '',
            'Edo': tarea.edo,
            'ND': tarea.nd,
            'Nombre del contacto': tarea.nombre_del_contacto,
            'Puesto o Cargo': tarea.puesto_o_cargo,
            'Tel. del Plantel': tarea.tel_plantel,
            'Ext': tarea.ext,
            'Celular': tarea.celular,
            'Email': tarea.email,
            'Estatus de la llamada': tarea.estatus_llamada,
            'UR': tarea.ur,
            'Observaciones': tarea.observaciones,
        }

        # Agregar registros de llamadas relacionados
        registros = RegistroLlamadas.objects.filter(ficha=tarea)
        for i, reg in enumerate(registros):
            task_data[f'NumLlamada_{i+1}'] = reg.NumLlamada
            task_data[f'Fecha de Llamada_{i+1}'] = reg.fecha_llamada
            task_data[f'Hora de Llamada_{i+1}'] = reg.hora_llamada
            task_data[f'Acuerdos/Compromisos_{i+1}'] = reg.acuerdos_compromisos
            task_data[f'Fecha Comprometida_{i+1}'] = reg.fecha_comprometida
            task_data[f'Observaciones Generales_{i+1}'] = reg.observaciones_generales

        data.append(task_data)

    # Convertir a DataFrame
    df = pd.DataFrame(data)

    # Crear workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Registros de Llamadas'

    # Crear estilos de fecha y hora
    date_style = NamedStyle(name='date_style', number_format='DD/MM/YYYY')
    time_style = NamedStyle(name='time_style', number_format='HH:MM:SS')
    datetime_style = NamedStyle(name='datetime_style', number_format='DD/MM/YYYY HH:MM:SS')

    # Registrar estilos (evita error si ya existen)
    for style in [date_style, time_style, datetime_style]:
        if style.name not in wb.named_styles:
            wb.add_named_style(style)

    # Agregar filas al Excel
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        ws.append(row)
        for c_idx, cell_value in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx)
            if isinstance(cell_value, datetime):
                cell.style = datetime_style
            elif isinstance(cell_value, date):
                cell.style = date_style
            elif isinstance(cell_value, time):
                cell.style = time_style

    # Crear respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="RegistrodeLlamadas.xlsx"'

    wb.save(response)
    return response


from django.shortcuts import render, get_object_or_404, redirect
from .models import DatosLlamadasInmuebles, RegistroLlamadas
from .forms import  RegistroLlamadasForm

@login_required
@permission_required('tasks.add_tasks_inmueble', raise_exception=True)
def tareas_list(request):
    search_query = request.GET.get("q", "")
    prioridad = request.GET.get("prioridad", "")
    ur = request.GET.get("ur", "")
    orden = request.GET.get("ordenar", "")

    tareas = DatosLlamadasInmuebles.objects.all()

    if search_query:
        tareas = tareas.filter(
            Q(NombreInmueble__icontains=search_query) |
            Q(rfi__icontains=search_query) |
            Q(edo__icontains=search_query) |
            Q(nd__icontains=search_query)
        )
    if prioridad:
        tareas = tareas.filter(prioridad=prioridad)
    if ur:
        tareas = tareas.filter(ur=ur)

    if orden == "az":
        tareas = tareas.order_by("NombreInmueble")
    elif orden == "za":
        tareas = tareas.order_by("-NombreInmueble")
    elif orden == "nuevo":
        tareas = tareas.order_by("-creado")
    elif orden == "viejo":
        tareas = tareas.order_by("creado")

    paginator = Paginator(tareas, 10)
    page = request.GET.get("page")
    llamadas = paginator.get_page(page)

    context = {
        "llamadas": llamadas,
        "search_query": search_query,
        "prioridad": prioridad,
        "ur": ur,
        "orden": orden,
        "ur_opciones": [op[0] for op in DatosLlamadasInmuebles.UR_CHOICES],
    }
    return render(request, "llamadas/tareas_list.html", context)

@login_required
@permission_required('tasks.add_tasks_inmueble', raise_exception=True)
def task_detail_llamadas(request, pk):
    tarea = get_object_or_404(DatosLlamadasInmuebles, pk=pk)
    registros = tarea.registro_llamadas.all().order_by("fecha_llamada")
    context = {
        "tarea": tarea,
        "registros": registros,
    }
    return render(request, "llamadas/task_detail.html", context)

@login_required
@permission_required('tasks.add_tasks_inmueble', raise_exception=True)
def registro_llamada(request, pk):
    tarea = get_object_or_404(DatosLlamadasInmuebles, pk=pk)
    if request.method == "POST":
        form = RegistroLlamadasForm(request.POST)
        if form.is_valid():
            llamada = form.save(commit=False)
            llamada.ficha = tarea
            llamada.save()
            return redirect("task_detail_llamadas", pk=tarea.id)
    else:
        form = RegistroLlamadasForm()

    context = {
        "form": form,
        "tarea": tarea,
    }
    return render(request, "llamadas/registro_llamada.html", context)


from django.shortcuts import render, redirect
from .forms import DatosLlamadasInmueblesForm

@login_required
@permission_required('tasks.add_tasks_inmueble', raise_exception=True)
def crear_tarea(request):
    if request.method == "POST":
        form = DatosLlamadasInmueblesForm(request.POST)
        if form.is_valid():
            tarea = form.save()
            return redirect("task_detail_llamadas", pk=tarea.id)  # Redirige al detalle de la tarea
    else:
        form = DatosLlamadasInmueblesForm()

    context = {
        "form": form,
    }
    return render(request, "llamadas/crear_tarea.html", context)


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Inmueble
from .forms import InmuebleForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

@login_required
@permission_required('tasks.view_inmueble', raise_exception=True)
def inmuebles_list(request):
    search_query = request.GET.get("q", "")
    prioridad = request.GET.get("prioridad", "")
    ur = request.GET.get("ur", "")
    orden = request.GET.get("ordenar", "")

    inmuebles = Inmueble.objects.all()

    # 🔎 Filtros de búsqueda
    if search_query:
        inmuebles = inmuebles.filter(
            Q(NombreInmueble__icontains=search_query) |
            Q(rfi__icontains=search_query) |
            Q(entidad_federativa__icontains=search_query) |
            Q(municipio_alcaldia__icontains=search_query)
        )
    if prioridad:
        inmuebles = inmuebles.filter(prioridad=prioridad)
    if ur:
        inmuebles = inmuebles.filter(UR=ur)

    # 🔃 Ordenamientos
    if orden == "az":
        inmuebles = inmuebles.order_by("NombreInmueble")
    elif orden == "za":
        inmuebles = inmuebles.order_by("-NombreInmueble")
    elif orden == "nuevo":
        inmuebles = inmuebles.order_by("-creado")
    elif orden == "viejo":
        inmuebles = inmuebles.order_by("creado")

    # 📊 Paginación
    paginator = Paginator(inmuebles, 30)
    page = request.GET.get("page")
    inmuebles_page = paginator.get_page(page)

    # ✅ Totales usando `datecompleted`
    total_completed_inmuebles = inmuebles.filter(datecompleted__isnull=False).count()
    total_pending_inmuebles = inmuebles.filter(datecompleted__isnull=True).count()

    context = {
        "inmuebles": inmuebles_page,
        "search_query": search_query,
        "prioridad": prioridad,
        "ur": ur,
        "orden": orden,
        "ur_opciones": [op[0] for op in Inmueble.UR_CHOICES],
        "total_completed_inmuebles": total_completed_inmuebles,
        "total_pending_inmuebles": total_pending_inmuebles,
    }
    return render(request, "Inmuebles/inmuebles_list.html", context)



# 🏠 Detalle y actualización de inmueble
@login_required
@permission_required('tasks.change_inmueble', raise_exception=True)
def detalle_inmueble(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)

    # Lógica para el formulario principal (inmueble)
    inmueble_form = InmuebleForm(request.POST or None, request.FILES or None, instance=inmueble)
    if 'inmueble_form_submit' in request.POST and inmueble_form.is_valid():
        if inmueble_form.cleaned_data.get('estado') == 'Completado' and not inmueble.datecompleted:
            inmueble.datecompleted = timezone.now()
        inmueble_form.save()
        messages.success(request, "El inmueble se actualizó correctamente ✅")
        # Redirige a la misma página, manteniendo la pestaña activa
        return redirect(f"{request.path}?tab=informacion")

    # Lógica para el formulario de Dictamenes
    dictamen_form = DictamenEstructuralIMPForm(request.POST or None, request.FILES or None)
    if 'dictamen_form_submit' in request.POST and dictamen_form.is_valid():
        new_dictamen = dictamen_form.save(commit=False)
        new_dictamen.task = inmueble
        new_dictamen.save()
        messages.success(request, "El dictamen se guardó correctamente ✅")
        # Redirige a la misma página, manteniendo la pestaña activa
        return redirect(f"{request.path}?tab=dictamenes")
    elif 'dictamen_form_submit' in request.POST and not dictamen_form.is_valid():
        messages.error(request, "Hubo un error al guardar el dictamen ❌")

    # Lógica para el formulario de Folios Reales
    folios_form = FoliosRealesIMPForm(request.POST or None, request.FILES or None)
    if 'folios_form_submit' in request.POST and folios_form.is_valid():
        new_folios = folios_form.save(commit=False)
        new_folios.task = inmueble
        new_folios.save()
        messages.success(request, "El folio real se guardó correctamente ✅")
        # Redirige a la misma página, manteniendo la pestaña activa
        return redirect(f"{request.path}?tab=dictamenes")
    elif 'folios_form_submit' in request.POST and not folios_form.is_valid():
        messages.error(request, "Hubo un error al guardar el folio real ❌")

    # Lógica para el formulario de Números de Plano
    planos_form = NumeroPlanoIMPForm(request.POST or None, request.FILES or None)
    if 'planos_form_submit' in request.POST and planos_form.is_valid():
        new_plano = planos_form.save(commit=False)
        new_plano.task = inmueble
        new_plano.save()
        messages.success(request, "El número de plano se guardó correctamente ✅")
        # Redirige a la misma página, manteniendo la pestaña activa
        return redirect(f"{request.path}?tab=dictamenes")
    elif 'planos_form_submit' in request.POST and not planos_form.is_valid():
        messages.error(request, "Hubo un error al guardar el número de plano ❌")

    # Lógica para el formulario de Expedientes CEDOC
    cedoc_form = Expedientes_CEDOCIMPForm(request.POST or None, request.FILES or None)
    if 'cedoc_form_submit' in request.POST and cedoc_form.is_valid():
        new_cedoc = cedoc_form.save(commit=False)
        new_cedoc.task = inmueble
        new_cedoc.save()
        messages.success(request, "El expediente CEDOC se guardó correctamente ✅")
        # Redirige a la misma página, manteniendo la pestaña activa
        return redirect(f"{request.path}?tab=dictamenes")
    elif 'cedoc_form_submit' in request.POST and not cedoc_form.is_valid():
        messages.error(request, "Hubo un error al guardar el expediente CEDOC ❌")

    # Lógica para el formulario de Títulos de Propiedad
    titulo_form = DocumentoPropiedadIMPForm(request.POST or None, request.FILES or None)
    if 'titulo_form_submit' in request.POST and titulo_form.is_valid():
        new_titulo = titulo_form.save(commit=False)
        new_titulo.task = inmueble
        new_titulo.save()
        messages.success(request, "El título de propiedad se guardó correctamente ✅")
        # Redirige a la misma página, manteniendo la pestaña activa
        return redirect(f"{request.path}?tab=titulos")
    elif 'titulo_form_submit' in request.POST and not titulo_form.is_valid():
        messages.error(request, "Hubo un error al guardar el título de propiedad ❌")
        
    # Lógica para el formulario de Observaciones
    observaciones_form = ObservacionesForm(request.POST or None, request.FILES or None)
    if 'observaciones_form_submit' in request.POST and observaciones_form.is_valid():
        new_observacion = observaciones_form.save(commit=False)
        new_observacion.task = inmueble
        new_observacion.save()
        messages.success(request, "La observación se guardó correctamente ✅")
        return redirect(f"{request.path}?tab=observaciones")
    elif 'observaciones_form_submit' in request.POST and not observaciones_form.is_valid():
        messages.error(request, "Hubo un error al guardar la observación ❌")

    # Si la solicitud no es POST, se inicializan los formularios
    if request.method != "POST":
        inmueble_form = InmuebleForm(instance=inmueble)
        dictamen_form = DictamenEstructuralIMPForm()
        folios_form = FoliosRealesIMPForm()
        planos_form = NumeroPlanoIMPForm()
        cedoc_form = Expedientes_CEDOCIMPForm()
        titulo_form = DocumentoPropiedadIMPForm()
        observaciones_form = ObservacionesForm()

    # Datos para la plantilla
    dictamenes = inmueble.dictamen_estructural.all()
    titulos = inmueble.docprop.all()
    folios_reales = inmueble.folios_reales.all()
    numeros_planos = inmueble.numeros_planos.all()
    expedientes_cedoc = inmueble.expedientes_deoc.all()
    observaciones_list = inmueble.observaciones.all()

    return render(request, "Inmuebles/detalle_inmueble.html", {
        "form": inmueble_form,
        "inmueble": inmueble,
        "dictamen_form": dictamen_form,
        "dictamenes": dictamenes,
        "titulo_form": titulo_form,
        "titulos": titulos,
        "folios_form": folios_form,
        "folios_reales": folios_reales,
        "planos_form": planos_form,
        "numeros_planos": numeros_planos,
        "cedoc_form": cedoc_form,
        "expedientes_cedoc": expedientes_cedoc,
        "observaciones_form": observaciones_form,
        "observaciones_list": observaciones_list,
    })
