import json
from django.shortcuts import render

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

from MDSJSEP.models import EventosCreados, Task_eventos
from tasks.forms import  CreateTaskSalasForm, SalasForm
# Create your views here.

# Create your views here.

def signupMDSJ(request):
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
                return render(request, 'signupMDSJ.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signupMDSJ.html', {"form": UserCreationForm, "error": "Passwords did not match."})
    

def signinMDSJ(request):
    if request.method == 'GET':
        return render(request, 'signinMDSJ.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signinMDSJ.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('calendar_MDSJ')


@login_required
def signout_MDSJ(request):
    logout(request)
    return redirect('signinMDSJ')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
def task_salas(request):
    
    tareas = Task_eventos.objects.all()
        
    return render(request, 'homeSalas.html', {
        'tareas' : tareas
    })

from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('MDSJSEP.add_evento', raise_exception=True)
def calendar_MDSJ(request):  
    eventos = EventosCreados.objects.all()
    all_events = EventosCreados.objects.all()
    return render(request,'extends_salas/calendar.html', {
        "events": all_events,
        "eventos": eventos,
    })


@login_required
def all_events_MDSJ(request):                                                                                                 
    selected_sala = request.GET.get('sala', None)
    
    # Filtra los eventos por sala si se proporciona una sala seleccionada
    if selected_sala:
        all_events = EventosCreados.objects.filter(Nom_sala=selected_sala)
    else:
        all_events = EventosCreados.objects.all()
    
    out = []                                                                                                             
    for event in all_events:  
        dia_formatted = event.dia.strftime("%Y-%m-%d") if event.dia else None                                                                                         
        out.append({                                                                                                     
            'title': event.title,
            'id': event.id,
            'start': dia_formatted + 'T' + event.hora_inicio.strftime("%H:%M") if event.hora_inicio else None,
            'end': dia_formatted + 'T' + event.hora_finalizacion.strftime("%H:%M") if event.hora_finalizacion else None,
            'Nom_sala': event.Nom_sala,
            'capacidad': event.capacidad,
            'nivel': event.nivel,
            'sala': event.sala,
            'prioridad': event.prioridad,
            'coordina': event.coordina,
            'preside': event.preside,
            'cargo': event.cargo,
            'no_personas': event.no_personas,
            'contacto': event.contacto,
            'servicios': event.servicios,
            'observaciones': event.observaciones,
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 

@login_required 
def add_event_MDSJ(request):
    dia = request.GET.get("dia", None)
    hora_inicio = request.GET.get("hora_inicio", None)
    hora_finalizacion = request.GET.get("hora_finalizacion", None)
    title = request.GET.get("title", None)
    prioridad = request.GET.get("prioridad", None)
    Nom_sala = request.GET.get("Nom_sala", None)
    nivel = request.GET.get("nivel", None)
    capacidad = request.GET.get("capacidad", None)
    sala = request.GET.get("sala", None)
    coordina = request.GET.get("coordina", None)
    preside = request.GET.get("preside", None)
    cargo = request.GET.get("cargo", None)
    no_personas = request.GET.get("no_personas", None)
    contacto = request.GET.get("contacto", None)
    servicios = request.GET.get("servicios", None)
    observaciones = request.GET.get("observaciones", None)
    
    event = EventosCreados(title=title, dia=dia, hora_inicio=hora_inicio, hora_finalizacion=hora_finalizacion, prioridad=prioridad, sala=sala, Nom_sala=Nom_sala, capacidad=capacidad, nivel=nivel, coordina=coordina, preside=preside, cargo=cargo, no_personas=no_personas,
                   contacto=contacto, servicios=servicios, observaciones=observaciones)
    event.save()
    data = {}
    return JsonResponse(data)

@login_required 
def update_MDSJ(request):
    if request.method == 'GET':
        dia = request.GET.get("dia", None)
        title = request.GET.get("title", None)
        event_id = request.GET.get("id", None)
        try:
            event = EventosCreados.objects.get(id=event_id)
            event.dia = dia
            event.title = title
            event.save()
            data = {'success': True}
        except EventosCreados.DoesNotExist:
            data = {'success': False, 'error_message': 'Evento no encontrado'}
    else:
        data = {'success': False, 'error_message': 'Solicitud no válida'}

    return JsonResponse(data)
 
@login_required 
def remove_MDSJ(request):
    if request.method == 'GET':
        event_id = request.GET.get("id", None)
        try:
            event = EventosCreados.objects.get(id=event_id)
            event.delete()
            data = {'success': True}
        except EventosCreados.DoesNotExist:
            data = {'success': False, 'error_message': 'Evento no encontrado'}
    else:
        data = {'success': False, 'error_message': 'Solicitud no válida'}

    return JsonResponse(data)


@login_required
def create_event(request):
    if request.method == 'POST':
        form = CreateTaskSalasForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('task_salas')  
    else:
        form = CreateTaskSalasForm()
    context = {'form': form}
    return render(request, 'create_event.html', context)



@login_required
def detail_event(request, task_id):
    task = get_object_or_404(Task_eventos, pk=task_id)
    
    if request.method == 'POST':
        form = SalasForm(request.POST, request.FILES, instance=task)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_salas')
        
    else:
        form = SalasForm(instance=task)
        
    return render(request, 'task_detail_event.html', {
        'task': task,
        'form': form,
    })

from django.shortcuts import render
from .models import EventosCreados
from django.db.models import Count, Sum, Avg, Q
import json
from django.utils.dateformat import format
from datetime import datetime, timedelta
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from django.db.models import Sum, Count, FloatField, IntegerField
from django.db.models.functions import Cast, Extract
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def uso_salas_view(request):
    from datetime import datetime
    
    eventos = EventosCreados.objects.all()
    
    # Filtramos los eventos para obtener solo las salas y el número total de asistentes
    datos_salas = eventos.values('Nom_sala', 'dia').annotate(
        total_usos=Count('Nom_sala'),
        no_personas=Sum(Cast('no_personas', FloatField()))  # Cast a FloatField
    )

    # Convertir la fecha a un formato de cadena (por ejemplo, 'YYYY-MM-DD')
    for sala in datos_salas:
        sala['dia'] = format(sala['dia'], 'Y-m-d')  # Cambia el formato si es necesario

    # Obtener años disponibles para el selector
    años_disponibles = eventos.values_list('dia__year', flat=True).distinct().order_by('-dia__year')
    if not años_disponibles:
        años_disponibles = [datetime.now().year]
    
    año_actual = datetime.now().year

    # Pasamos los datos a JSON
    datos_json = json.dumps(list(datos_salas))
    return render(request, 'uso_salas.html', {
        'datos_salas': datos_json,
        'años': años_disponibles,
        'año_actual': año_actual
    })

@login_required
def export_reporte_trimestral_salas(request):
    """
    Genera un reporte trimestral Excel con estadísticas detalladas del uso de salas de juntas.
    Incluye resumen general, estadísticas por sala, totales, y comparativas.
    """
    # Obtener parámetros del request
    trimestre = request.GET.get('trimestre', None)
    año = request.GET.get('año', datetime.now().year)
    
    try:
        año = int(año)
        if trimestre:
            trimestre = int(trimestre)
    except (ValueError, TypeError):
        trimestre = None
        año = datetime.now().year
    
    # Definir rangos de fechas del trimestre
    if trimestre:
        if trimestre == 1:
            fecha_inicio = datetime(año, 1, 1)
            fecha_fin = datetime(año, 3, 31, 23, 59, 59)
            nombre_trimestre = f"Q1 {año} (Ene-Mar)"
        elif trimestre == 2:
            fecha_inicio = datetime(año, 4, 1)
            fecha_fin = datetime(año, 6, 30, 23, 59, 59)
            nombre_trimestre = f"Q2 {año} (Abr-Jun)"
        elif trimestre == 3:
            fecha_inicio = datetime(año, 7, 1)
            fecha_fin = datetime(año, 9, 30, 23, 59, 59)
            nombre_trimestre = f"Q3 {año} (Jul-Sep)"
        elif trimestre == 4:
            fecha_inicio = datetime(año, 10, 1)
            fecha_fin = datetime(año, 12, 31, 23, 59, 59)
            nombre_trimestre = f"Q4 {año} (Oct-Dic)"
        else:
            fecha_inicio = None
            fecha_fin = None
            nombre_trimestre = f"Todos los períodos - {año}"
    else:
        fecha_inicio = datetime(año, 1, 1)
        fecha_fin = datetime(año, 12, 31, 23, 59, 59)
        nombre_trimestre = f"Año completo {año}"
    
    # Filtrar eventos por rango de fechas
    if fecha_inicio and fecha_fin:
        eventos = EventosCreados.objects.filter(
            dia__gte=fecha_inicio,
            dia__lte=fecha_fin
        )
    else:
        eventos = EventosCreados.objects.filter(dia__year=año)
    
    # Crear workbook y hojas
    wb = Workbook()
    
    # Estilos
    header_fill = PatternFill(start_color="691C32", end_color="691C32", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    title_font = Font(bold=True, size=14, color="691C32")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    center_alignment = Alignment(horizontal='center', vertical='center')
    
    # HOJA 1: Resumen General
    ws1 = wb.active
    ws1.title = "Resumen General"
    
    # Título
    ws1.merge_cells('A1:D1')
    ws1['A1'] = f"REPORTE TRIMESTRAL - USO DE SALAS DE JUNTAS"
    ws1['A1'].font = title_font
    ws1['A1'].alignment = center_alignment
    
    ws1.merge_cells('A2:D2')
    ws1['A2'] = nombre_trimestre
    ws1['A2'].font = Font(size=11, italic=True)
    ws1['A2'].alignment = center_alignment
    
    ws1.append([])
    
    # Estadísticas generales
    total_eventos = eventos.count()
    total_personas = sum(int(e.no_personas or 0) for e in eventos if e.no_personas and str(e.no_personas).isdigit())
    total_salas_utilizadas = eventos.values('Nom_sala').distinct().count()
    promedio_personas = total_personas / total_eventos if total_eventos > 0 else 0
    
    stats = [
        ['INDICADOR', 'VALOR'],
        ['Total de Eventos', total_eventos],
        ['Total de Personas', total_personas],
        ['Salas Utilizadas', total_salas_utilizadas],
        ['Promedio de Personas por Evento', round(promedio_personas, 2)],
    ]
    
    row_idx = 4
    for stat in stats:
        ws1.append(stat)
        for col in range(1, 3):
            cell = ws1.cell(row=row_idx, column=col)
            cell.border = border
            if row_idx == 4:  # Header
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = center_alignment
            else:
                cell.alignment = Alignment(horizontal='left' if col == 1 else 'right', vertical='center')
        row_idx += 1
    
    ws1.column_dimensions['A'].width = 35
    ws1.column_dimensions['B'].width = 20
    
    # HOJA 2: Estadísticas por Sala
    ws2 = wb.create_sheet("Estadísticas por Sala")
    
    ws2.merge_cells('A1:G1')
    ws2['A1'] = f"ESTADÍSTICAS POR SALA - {nombre_trimestre}"
    ws2['A1'].font = title_font
    ws2['A1'].alignment = center_alignment
    ws2.append([])
    
    # Encabezados
    headers = ['Sala', 'Total Eventos', 'Total Personas', 'Promedio Personas/Evento', 'Capacidad', 'Tasa de Ocupación %', 'Nivel']
    ws2.append(headers)
    
    # Aplicar estilo a encabezados
    for col in range(1, len(headers) + 1):
        cell = ws2.cell(row=3, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_alignment
        cell.border = border
    
    # Obtener estadísticas por sala
    salas_stats = eventos.values('Nom_sala', 'capacidad', 'nivel').annotate(
        total_eventos=Count('id'),
        total_personas=Sum(Cast('no_personas', IntegerField()))
    ).order_by('-total_eventos')
    
    row_idx = 4
    for sala_stat in salas_stats:
        nom_sala = sala_stat['Nom_sala'] or 'Sin nombre'
        total_eventos_sala = sala_stat['total_eventos']
        total_personas_sala = sala_stat['total_personas'] or 0
        promedio_sala = total_personas_sala / total_eventos_sala if total_eventos_sala > 0 else 0
        capacidad = sala_stat['capacidad'] or 'N/A'
        nivel = sala_stat['nivel'] or 'N/A'
        
        # Calcular tasa de ocupación promedio (personas promedio vs capacidad)
        try:
            capacidad_num = int(capacidad)
            if capacidad_num > 0 and total_eventos_sala > 0:
                # Tasa de ocupación = (promedio de personas) / capacidad * 100
                tasa_ocupacion = (promedio_sala / capacidad_num) * 100
            else:
                tasa_ocupacion = 0
        except (ValueError, TypeError):
            tasa_ocupacion = 'N/A'
        
        row_data = [
            nom_sala,
            total_eventos_sala,
            total_personas_sala,
            round(promedio_sala, 2),
            capacidad,
            round(tasa_ocupacion, 2) if isinstance(tasa_ocupacion, (int, float)) else tasa_ocupacion,
            nivel
        ]
        
        ws2.append(row_data)
        
        # Aplicar estilos
        for col in range(1, len(row_data) + 1):
            cell = ws2.cell(row=row_idx, column=col)
            cell.border = border
            if col == 1:
                cell.alignment = Alignment(horizontal='left', vertical='center')
            else:
                cell.alignment = Alignment(horizontal='center', vertical='center')
        row_idx += 1
    
    # Ajustar anchos de columna
    ws2.column_dimensions['A'].width = 40
    for col in range(2, 8):
        ws2.column_dimensions[get_column_letter(col)].width = 18
    
    # HOJA 3: Detalle de Eventos
    ws3 = wb.create_sheet("Detalle de Eventos")
    
    ws3.merge_cells('A1:J1')
    ws3['A1'] = f"DETALLE DE EVENTOS - {nombre_trimestre}"
    ws3['A1'].font = title_font
    ws3['A1'].alignment = center_alignment
    ws3.append([])
    
    # Encabezados
    headers_detalle = ['Fecha', 'Hora Inicio', 'Hora Fin', 'Título', 'Sala', 'Personas', 'Coordina', 'Preside', 'Prioridad', 'Contacto']
    ws3.append(headers_detalle)
    
    # Aplicar estilo a encabezados
    for col in range(1, len(headers_detalle) + 1):
        cell = ws3.cell(row=3, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_alignment
        cell.border = border
    
    # Datos de eventos
    eventos_ordenados = eventos.order_by('dia', 'hora_inicio')
    row_idx = 4
    for evento in eventos_ordenados:
        fecha = evento.dia.strftime('%d/%m/%Y') if evento.dia else 'N/A'
        hora_inicio = evento.hora_inicio.strftime('%H:%M') if evento.hora_inicio else 'N/A'
        hora_fin = evento.hora_finalizacion.strftime('%H:%M') if evento.hora_finalizacion else 'N/A'
        
        row_data = [
            fecha,
            hora_inicio,
            hora_fin,
            evento.title or 'Sin título',
            evento.Nom_sala or 'N/A',
            evento.no_personas or 0,
            evento.coordina or 'N/A',
            evento.preside or 'N/A',
            evento.prioridad or 'N/A',
            evento.contacto or 'N/A'
        ]
        
        ws3.append(row_data)
        
        # Aplicar estilos
        for col in range(1, len(row_data) + 1):
            cell = ws3.cell(row=row_idx, column=col)
            cell.border = border
            cell.alignment = Alignment(horizontal='center' if col != 4 and col != 7 and col != 8 else 'left', vertical='center')
        row_idx += 1
    
    # Ajustar anchos de columna
    ws3.column_dimensions['A'].width = 12
    ws3.column_dimensions['B'].width = 12
    ws3.column_dimensions['C'].width = 12
    ws3.column_dimensions['D'].width = 30
    ws3.column_dimensions['E'].width = 30
    for col in range(6, 11):
        ws3.column_dimensions[get_column_letter(col)].width = 18
    
    # HOJA 4: Comparativa Mensual
    ws4 = wb.create_sheet("Comparativa Mensual")
    
    ws4.merge_cells('A1:E1')
    ws4['A1'] = f"COMPARATIVA MENSUAL - {año}"
    ws4['A1'].font = title_font
    ws4['A1'].alignment = center_alignment
    ws4.append([])
    
    headers_mensual = ['Mes', 'Total Eventos', 'Total Personas', 'Promedio Personas/Evento', 'Salas Utilizadas']
    ws4.append(headers_mensual)
    
    # Aplicar estilo a encabezados
    for col in range(1, len(headers_mensual) + 1):
        cell = ws4.cell(row=3, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_alignment
        cell.border = border
    
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    row_idx = 4
    eventos_año = EventosCreados.objects.filter(dia__year=año)
    
    for mes_num, mes_nombre in meses.items():
        eventos_mes = eventos_año.filter(dia__month=mes_num)
        total_eventos_mes = eventos_mes.count()
        total_personas_mes = sum(int(e.no_personas or 0) for e in eventos_mes if e.no_personas and str(e.no_personas).isdigit())
        promedio_mes = total_personas_mes / total_eventos_mes if total_eventos_mes > 0 else 0
        salas_mes = eventos_mes.values('Nom_sala').distinct().count()
        
        row_data = [
            mes_nombre,
            total_eventos_mes,
            total_personas_mes,
            round(promedio_mes, 2),
            salas_mes
        ]
        
        ws4.append(row_data)
        
        # Aplicar estilos
        for col in range(1, len(row_data) + 1):
            cell = ws4.cell(row=row_idx, column=col)
            cell.border = border
            cell.alignment = Alignment(horizontal='center' if col != 1 else 'left', vertical='center')
        row_idx += 1
    
    # Ajustar anchos de columna
    ws4.column_dimensions['A'].width = 15
    for col in range(2, 6):
        ws4.column_dimensions[get_column_letter(col)].width = 20
    
    # Preparar respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"Reporte_Trimestral_Salas_{nombre_trimestre.replace(' ', '_')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    wb.save(response)
    return response

def create_table_pdf(data, col_widths=None, styles=None):
    """Función auxiliar para crear tablas PDF con estilo"""
    if styles is None:
        styles = getSampleStyleSheet()
    
    # Crear estilo personalizado para headers con texto blanco
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        textColor=colors.white,
        fontName='Helvetica-Bold',
        fontSize=9,
        alignment=0,  # LEFT
    )
    
    # Convertir datos a Paragraphs para permitir saltos de línea
    table_data = []
    for row_idx, row in enumerate(data):
        table_row = []
        for col_idx, cell_value in enumerate(row):
            if row_idx == 0:  # Header
                # Usar estilo personalizado con texto blanco para headers
                para = Paragraph(f"<b>{str(cell_value)}</b>", header_style)
            else:
                # Convertir a string y usar Paragraph para permitir saltos
                para = Paragraph(str(cell_value), styles['Normal'])
            table_row.append(para)
        table_data.append(table_row)
    
    if col_widths is None:
        # Calcular anchos automáticos basados en el número de columnas
        num_cols = len(data[0]) if data else 0
        if num_cols > 0:
            # A4 width = 8.27 inches, dejar espacio para márgenes (aproximadamente 7.27 inches útiles)
            total_width = 7.27 * inch
            col_width = total_width / num_cols
            col_widths = [col_width] * num_cols
    
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#691c32")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#ffffff")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f9f9f9"), colors.white]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1), True),  # Permitir saltos de línea automáticos
    ]))
    return table

@login_required
def export_reporte_trimestral_salas_pdf(request):
    """
    Genera un reporte trimestral PDF con estadísticas detalladas del uso de salas de juntas.
    Incluye filtros por nombre de sala, más utilizadas, más personas, etc.
    """
    # Obtener parámetros del request
    trimestre = request.GET.get('trimestre', None)
    año = request.GET.get('año', datetime.now().year)
    nombre_sala = request.GET.get('nombre_sala', None)
    filtro_orden = request.GET.get('filtro_orden', 'total_eventos')  # total_eventos, total_personas
    top_n = request.GET.get('top_n', None)
    
    try:
        año = int(año)
        if trimestre:
            trimestre = int(trimestre)
        if top_n:
            top_n = int(top_n)
    except (ValueError, TypeError):
        trimestre = None
        año = datetime.now().year
        top_n = None
    
    # Definir rangos de fechas del trimestre
    if trimestre:
        if trimestre == 1:
            fecha_inicio = datetime(año, 1, 1)
            fecha_fin = datetime(año, 3, 31, 23, 59, 59)
            nombre_trimestre = f"Q1 {año} (Enero-Marzo)"
        elif trimestre == 2:
            fecha_inicio = datetime(año, 4, 1)
            fecha_fin = datetime(año, 6, 30, 23, 59, 59)
            nombre_trimestre = f"Q2 {año} (Abril-Junio)"
        elif trimestre == 3:
            fecha_inicio = datetime(año, 7, 1)
            fecha_fin = datetime(año, 9, 30, 23, 59, 59)
            nombre_trimestre = f"Q3 {año} (Julio-Septiembre)"
        elif trimestre == 4:
            fecha_inicio = datetime(año, 10, 1)
            fecha_fin = datetime(año, 12, 31, 23, 59, 59)
            nombre_trimestre = f"Q4 {año} (Octubre-Diciembre)"
        else:
            fecha_inicio = datetime(año, 1, 1)
            fecha_fin = datetime(año, 12, 31, 23, 59, 59)
            nombre_trimestre = f"Año completo {año}"
    else:
        fecha_inicio = datetime(año, 1, 1)
        fecha_fin = datetime(año, 12, 31, 23, 59, 59)
        nombre_trimestre = f"Año completo {año}"
    
    # Filtrar eventos por rango de fechas
    if fecha_inicio and fecha_fin:
        eventos = EventosCreados.objects.filter(
            dia__gte=fecha_inicio,
            dia__lte=fecha_fin
        )
    else:
        eventos = EventosCreados.objects.filter(dia__year=año)
    
    # Filtrar por nombre de sala si se especifica
    if nombre_sala:
        eventos = eventos.filter(Nom_sala=nombre_sala)
    
    # Crear respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    filename = f"Reporte_Trimestral_Salas_{nombre_trimestre.replace(' ', '_')}"
    if nombre_sala:
        filename += f"_{nombre_sala.replace(' ', '_')}"
    response['Content-Disposition'] = f'inline; filename="{filename}.pdf"'
    
    # Crear el PDF
    pdf = SimpleDocTemplate(response, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para títulos
    title_style = styles['Title']
    title_style.textColor = colors.HexColor("#691c32")
    title_style.fontSize = 16
    title_style.spaceAfter = 12
    
    heading_style = styles['Heading2']
    heading_style.textColor = colors.HexColor("#691c32")
    heading_style.fontSize = 12
    heading_style.spaceAfter = 8
    
    # Título principal
    elements.append(Paragraph("<b>REPORTE TRIMESTRAL</b>", title_style))
    elements.append(Paragraph("<b>USO DE SALAS DE JUNTAS</b>", title_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Información del período
    periodo_text = f"<b>Período:</b> {nombre_trimestre}"
    if nombre_sala:
        periodo_text += f"<br/><b>Sala:</b> {nombre_sala}"
    elements.append(Paragraph(periodo_text, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # SECCIÓN 1: RESUMEN GENERAL
    elements.append(Paragraph("<b>RESUMEN GENERAL</b>", heading_style))
    
    total_eventos = eventos.count()
    total_personas = sum(int(e.no_personas or 0) for e in eventos if e.no_personas and str(e.no_personas).isdigit())
    total_salas_utilizadas = eventos.values('Nom_sala').distinct().count()
    promedio_personas = total_personas / total_eventos if total_eventos > 0 else 0
    
    resumen_data = [
        ['INDICADOR', 'VALOR'],
        ['Total de Eventos', f'{total_eventos:,}'],
        ['Total de Personas', f'{total_personas:,}'],
        ['Salas Utilizadas', f'{total_salas_utilizadas:,}'],
        ['Promedio de Personas por Evento', f'{promedio_personas:.2f}'],
    ]
    
    elements.append(create_table_pdf(resumen_data, col_widths=[3.5*inch, 2*inch], styles=styles))
    elements.append(Spacer(1, 0.3*inch))
    
    # SECCIÓN 2: ESTADÍSTICAS POR SALA
    elements.append(Paragraph("<b>ESTADÍSTICAS POR SALA</b>", heading_style))
    
    # Obtener estadísticas por sala
    salas_stats = eventos.values('Nom_sala', 'capacidad', 'nivel').annotate(
        total_eventos=Count('id'),
        total_personas=Sum(Cast('no_personas', IntegerField()))
    )
    
    # Ordenar según filtro
    if filtro_orden == 'total_personas':
        salas_stats = salas_stats.order_by('-total_personas')
        orden_desc = "ordenadas por Total de Personas (descendente)"
    elif filtro_orden == 'promedio_personas':
        # Calcular promedio para ordenar
        salas_list = list(salas_stats)
        for sala in salas_list:
            sala['promedio'] = sala['total_personas'] / sala['total_eventos'] if sala['total_eventos'] > 0 else 0
        salas_list.sort(key=lambda x: x['promedio'], reverse=True)
        salas_stats = salas_list
        orden_desc = "ordenadas por Promedio de Personas por Evento (descendente)"
    else:  # total_eventos (por defecto)
        salas_stats = salas_stats.order_by('-total_eventos')
        orden_desc = "ordenadas por Total de Eventos (descendente)"
    
    # Limitar a top N si se especifica
    if top_n:
        salas_stats = list(salas_stats)[:top_n]
        orden_desc += f" (Top {top_n})"
    
    # Crear tabla de estadísticas por sala
    stats_data = [
        ['Sala', 'Eventos', 'Total<br/>Personas', 'Promedio', 'Capacidad', 'Tasa<br/>Ocup. %', 'Nivel']
    ]
    
    for sala_stat in salas_stats:
        nom_sala = sala_stat['Nom_sala'] or 'Sin nombre'
        total_eventos_sala = sala_stat['total_eventos']
        total_personas_sala = sala_stat['total_personas'] or 0
        promedio_sala = total_personas_sala / total_eventos_sala if total_eventos_sala > 0 else 0
        capacidad = sala_stat['capacidad'] or 'N/A'
        nivel = sala_stat['nivel'] or 'N/A'
        
        # Calcular tasa de ocupación
        try:
            capacidad_num = int(capacidad)
            if capacidad_num > 0 and total_eventos_sala > 0:
                tasa_ocupacion = (promedio_sala / capacidad_num) * 100
                tasa_str = f'{tasa_ocupacion:.1f}%'
            else:
                tasa_str = 'N/A'
        except (ValueError, TypeError):
            tasa_str = 'N/A'
        
        # Usar el nombre completo, el Paragraph se encargará de los saltos de línea
        stats_data.append([
            nom_sala,
            str(total_eventos_sala),
            f'{int(total_personas_sala):,}',
            f'{promedio_sala:.2f}',
            str(capacidad),
            tasa_str,
            str(nivel)
        ])
    
    elements.append(Paragraph(f"<i>{orden_desc}</i>", styles['Normal']))
    elements.append(Spacer(1, 0.1*inch))
    # Ajustar anchos para que quepan en A4: 7.27 inches disponibles, dividir entre 7 columnas
    elements.append(create_table_pdf(stats_data, col_widths=[2.2*inch, 0.6*inch, 0.8*inch, 0.6*inch, 0.6*inch, 0.7*inch, 0.6*inch], styles=styles))
    elements.append(Spacer(1, 0.3*inch))
    
    # SECCIÓN 3: COMPARATIVA MENSUAL
    elements.append(Paragraph("<b>COMPARATIVA MENSUAL</b>", heading_style))
    
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    eventos_año = EventosCreados.objects.filter(dia__year=año)
    if nombre_sala:
        eventos_año = eventos_año.filter(Nom_sala=nombre_sala)
    
    mensual_data = [
        ['Mes', 'Total<br/>Eventos', 'Total<br/>Personas', 'Promedio<br/>Personas', 'Salas<br/>Utilizadas']
    ]
    
    for mes_num, mes_nombre in meses.items():
        eventos_mes = eventos_año.filter(dia__month=mes_num)
        total_eventos_mes = eventos_mes.count()
        total_personas_mes = sum(int(e.no_personas or 0) for e in eventos_mes if e.no_personas and str(e.no_personas).isdigit())
        promedio_mes = total_personas_mes / total_eventos_mes if total_eventos_mes > 0 else 0
        salas_mes = eventos_mes.values('Nom_sala').distinct().count()
        
        mensual_data.append([
            mes_nombre,
            str(total_eventos_mes),
            f'{int(total_personas_mes):,}',
            f'{promedio_mes:.2f}',
            str(salas_mes)
        ])
    
    # Ajustar anchos para que quepan en A4: dividir 7.27 inches entre 5 columnas
    elements.append(create_table_pdf(mensual_data, col_widths=[1.3*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch], styles=styles))
    elements.append(Spacer(1, 0.3*inch))
    
    # SECCIÓN 4: TOP SALAS (si no se filtró por nombre)
    if not nombre_sala:
        elements.append(PageBreak())
        elements.append(Paragraph("<b>RANKING DE SALAS</b>", heading_style))
        
        # Top 10 más utilizadas
        top_utilizadas = eventos.values('Nom_sala').annotate(
            total_eventos=Count('id')
        ).order_by('-total_eventos')[:10]
        
        top_data = [['Ranking', 'Sala', 'Total<br/>Eventos']]
        for idx, sala in enumerate(top_utilizadas, 1):
            nom_sala_top = sala['Nom_sala'] or 'Sin nombre'
            top_data.append([
                f'#{idx}',
                nom_sala_top,  # El Paragraph se encargará de los saltos de línea
                str(sala['total_eventos'])
            ])
        
        elements.append(Paragraph("<b>Top 10 Salas Más Utilizadas</b>", styles['Heading3']))
        # Ajustar anchos: 7.27 inches disponibles para 3 columnas
        elements.append(create_table_pdf(top_data, col_widths=[0.7*inch, 4.5*inch, 1.5*inch], styles=styles))
        elements.append(Spacer(1, 0.2*inch))
        
        # Top 10 con más personas
        top_personas = eventos.values('Nom_sala').annotate(
            total_personas=Sum(Cast('no_personas', IntegerField()))
        ).order_by('-total_personas')[:10]
        
        top_personas_data = [['Ranking', 'Sala', 'Total<br/>Personas']]
        for idx, sala in enumerate(top_personas, 1):
            nom_sala_top = sala['Nom_sala'] or 'Sin nombre'
            total_p = sala['total_personas'] or 0
            top_personas_data.append([
                f'#{idx}',
                nom_sala_top,  # El Paragraph se encargará de los saltos de línea
                f'{int(total_p):,}'
            ])
        
        elements.append(Paragraph("<b>Top 10 Salas con Más Personas</b>", styles['Heading3']))
        # Ajustar anchos: 7.27 inches disponibles para 3 columnas
        elements.append(create_table_pdf(top_personas_data, col_widths=[0.7*inch, 4.5*inch, 1.5*inch], styles=styles))
    
    # Construir PDF
    pdf.build(elements)
    return response
