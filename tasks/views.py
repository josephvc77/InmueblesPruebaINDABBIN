
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

from .forms import BajaForm, ColindanciasFormIMP, DatosAvaluosFormIMP, DatosTercerosFormIMP, DictamenEstructuralForm, DocumentoOcupacionFormIMP, DocumentoPropiedadFormIMP, EdificacionFormIMP, Edificio_VerdeFormIMP, Expedientes_CEDOCFormIMP, FoliosRealesFormIMP, InmuebleForm, InstitucionesOcupantesFormIMP, MensajeFormIMP, Numero_PlanoFormIMP, OcupacionesFormIMP, PasswordConfirmationForm, TramitesDisposicionFormIMP
from .models import ColindanciasIMP, DatosAvaluosIMP, DatosTercerosIMP, DictamenEstructuralIMP, Documento_ocupacionIMP, DocumentoPropiedadIMP, EdificacionIMP, EdificioVerdeIMP, Events, Expedientes_CEDOCIMP, FoliosRealesIMP, Inmueble, InstitucionesOcupantesIMP, MensajeIMP, NumeroPlanoIMP, OcupacionesIMP, TramitesDisposicionIMP

from .forms import TaskCreateForm

# Create your views here.

# Vista para cerrar sesión automáticamente
from django.contrib.auth import logout



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






def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('/')





    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         user = form.get_user()
    #         login(request, user)
    #         return redirect('tasks_importados')
    # else:
    #     form = AuthenticationForm()
    
    # return render(request, 'signin.html', {"form": form})
        


@login_required
def signout(request):
    logout(request)
    return redirect('signin')
    
from django.http import JsonResponse
from datetime import datetime
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


@login_required
def tasks_importados(request):
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')
    ur = request.GET.get('ur', '')
    orden = request.GET.get('ordenar', '')
    
    request.session['search_query'] = search_query
    request.session['prioridad'] = prioridad
    request.session['ur'] = ur
    request.session['ordenar'] = orden

    mensajes = MensajeIMP.objects.all()
    
    eventos = Events.objects.all()
    
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
    ).order_by('-updated')

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
        inmuebles_list = inmuebles_list.order_by('-updated')
    elif orden == 'viejo':
        inmuebles_list = inmuebles_list.order_by('creado')
        
    paginator = Paginator(inmuebles_list, 20)  # Muestra 20 inmuebles por página

    page = request.GET.get('page')
    inmuebles = paginator.get_page(page)
        
        
    for task in inmuebles:
        if task.deadline:
            now = datetime.now(timezone.utc)  # Usa la zona horaria UTC para now
            time_remaining = task.deadline - now
            days_remaining = time_remaining.days
            seconds_remaining = time_remaining.seconds
            hours_remaining, seconds_remaining = divmod(seconds_remaining, 3600)  # Convertir segundos en horas y segundos sobrantes
            # Calcular los días y las horas de retraso
            if days_remaining < 0:
                days_delayed = abs(days_remaining)
                hours_delayed = hours_remaining
            else:
                days_delayed = 0
                hours_delayed = 0

            # Agregar los valores calculados al objeto de tarea
            task.days_remaining = days_remaining
            task.hours_remaining = hours_remaining
            task.days_delayed = days_delayed
            task.hours_delayed = hours_delayed

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
        'mensajes' : mensajes, 
        'prioridad': prioridad,
        'ur': ur,
        'eventos' : eventos,
        'orden': orden,
    })
    
@login_required
def calendar(request):  
    mensajes = MensajeIMP.objects.all()
    eventos = Events.objects.all()
    all_events = Events.objects.all()

    return render(request,'calendar.html', {
        'mensajes' : mensajes,
        "events":all_events,
        "eventos" : eventos,
    })

@login_required
def all_events(request):                                                                                                 
    all_events = Events.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 

@login_required 
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)
 
@login_required 
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)



@login_required
def principal(request):
    return render(request, 'tasks.html')



@login_required
def inmuebles_baja_importados(request):
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')
    mensajes = MensajeIMP.objects.all()
    eventos = Events.objects.all()

    inmuebles_list = Inmueble.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        estado='Baja'  # Filtra los inmuebles con estado 'Baja'
    )

    if prioridad:
        inmuebles_list = inmuebles_list.filter(prioridad=prioridad)

    paginator = Paginator(inmuebles_list, 20)  # Muestra 20 inmuebles por página

    page = request.GET.get('page')
    try:
        inmuebles = paginator.page(page)
    except PageNotAnInteger:
        inmuebles = paginator.page(1)
    except EmptyPage:
        inmuebles = paginator.page(paginator.num_pages)

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
        'eventos': eventos,
    })

@login_required
def tasks_completed_importados(request):
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')
    ur = request.GET.get('ur', '')
    orden = request.GET.get('ordenar', '')
    
    mensajes = MensajeIMP.objects.all()
    eventos = Events.objects.all()

    # Filtra los inmuebles completados y aplica los filtros de búsqueda
    inmuebles_list = Inmueble.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        datecompleted__isnull=False
    ).order_by('-datecompleted')

    if prioridad:
        inmuebles_list = inmuebles_list.filter(prioridad=prioridad)
        
    if ur:
        inmuebles_list = inmuebles_list.filter(UR=ur)

    # Aplica filtros de orden
    if orden == 'az':
        inmuebles_list = inmuebles_list.order_by('NombreInmueble')
    elif orden == 'za':
        inmuebles_list = inmuebles_list.order_by('-NombreInmueble')
    elif orden == 'nuevo':
        inmuebles_list = inmuebles_list.order_by('-datecompleted')
    elif orden == 'viejo':
        inmuebles_list = inmuebles_list.order_by('datecompleted')

    paginator = Paginator(inmuebles_list, 20)  # Muestra 20 inmuebles completados por página

    page = request.GET.get('page')
    try:
        inmuebles = paginator.page(page)
    except PageNotAnInteger:
        inmuebles = paginator.page(1)
    except EmptyPage:
        inmuebles = paginator.page(paginator.num_pages)

    total_completed_inmuebles = Inmueble.objects.filter(datecompleted__isnull=False).count()  # Total de inmuebles completados
    
    total_pending_inmuebles = Inmueble.objects.filter(datecompleted__isnull=True).count()  # Total de inmuebles pendientes por completar

    return render(request, 'importados.html', {
        'inmuebles': inmuebles,
        'search_query': search_query,
        'total_completed_inmuebles': total_completed_inmuebles,
        'total_pending_inmuebles': total_pending_inmuebles,
        'mensajes': mensajes,
        'eventos': eventos,
        'prioridad': prioridad,
        'ur': ur,
        'orden': orden,
    })
    
@login_required
def bajas_importados(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    if task.estado == 'Activo':
        if request.method == 'POST':
            form = BajaForm(request.POST)
            if form.is_valid():
                task.estado = 'Baja'
                task.save()
                return redirect('inmuebles_baja_importados')
        else:
            form = BajaForm()

@login_required
def complete_task_importados(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks_importados')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskCreateForm

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            # Asignar la tarea al usuario seleccionado (si se ha seleccionado)
            assigned_to = form.cleaned_data['assigned_to']
            if assigned_to:
                task.assigned_to = assigned_to
                task.user = assigned_to  # Asignar la tarea al usuario seleccionado
            else:
                task.user = request.user  # El usuario actual crea la tarea
            task.save()
            return redirect('tasks_importados')
    else:
        form = TaskCreateForm(user=request.user)
    context = {'form': form}
    return render(request, 'create_task.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Inmueble
from .forms import InmuebleForm

@login_required
def task_detail_importados(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    
    if request.method == 'POST':
        inmueble = InmuebleForm(request.POST, request.FILES, instance=task)
        edificio_verde_form = Edificio_VerdeFormIMP(request.POST)
        documento_propiedad_form = DocumentoPropiedadFormIMP(request.POST, request.FILES)
        datos_avaluos_form = DatosAvaluosFormIMP(request.POST)
        ocupaciones_form = OcupacionesFormIMP(request.POST)
        documento_ocupacion_form = DocumentoOcupacionFormIMP(request.POST)
        instituciones_ocupantes_form = InstitucionesOcupantesFormIMP(request.POST)
        datos_terceros_form = DatosTercerosFormIMP(request.POST)
        colindancia_form = ColindanciasFormIMP(request.POST)
        tramite_disposicion_form = TramitesDisposicionFormIMP(request.POST)
        edificacion_form = EdificacionFormIMP(request.POST)
        mensaje_form = MensajeFormIMP(request.POST, prefix='mensaje')
        
        if documento_propiedad_form.is_valid():
            # Validación adicional para verificar si hay datos antes de guardar
            if any(documento_propiedad_form.cleaned_data.values()):
                documento_propiedad = documento_propiedad_form.save(commit=False)
                documento_propiedad.task = task
                documento_propiedad.save()
                return redirect('task_detail_importados', task_id=task_id)
        
        if datos_avaluos_form.is_valid():
            if any(datos_avaluos_form.cleaned_data.values()):
                datos_avaluo = datos_avaluos_form.save(commit=False)
                datos_avaluo.task = task
                datos_avaluo.save()
                return redirect('task_detail_importados', task_id=task_id)
            
        if mensaje_form.is_valid():
            mensaje_form.instance.enviado_por_imp = request.user
            if any(mensaje_form.cleaned_data.values()):
                mensaje = mensaje_form.save(commit=False)
                mensaje.task = task
                mensaje.save()
                return redirect('tasks_importados')
        
        if ocupaciones_form.is_valid():
            if any(ocupaciones_form.cleaned_data.values()):
                ocupaciones = ocupaciones_form.save(commit=False)
                ocupaciones.task = task
                ocupaciones.save()
                return redirect('task_detail_importados', task_id=task_id)
            
        if documento_ocupacion_form.is_valid():
            if any(documento_ocupacion_form.cleaned_data.values()):
                documento_ocupacion = documento_ocupacion_form.save(commit=False)
                documento_ocupacion.task = task
                documento_ocupacion.save()
                return redirect('task_detail_importados', task_id=task_id)
            
        if instituciones_ocupantes_form.is_valid():
            if any(instituciones_ocupantes_form.cleaned_data.values()):
                instituciones_ocupantes = instituciones_ocupantes_form.save(commit=False)
                instituciones_ocupantes.task = task
                instituciones_ocupantes.save()
                return redirect('task_detail_importados', task_id=task_id)
        
        if datos_terceros_form.is_valid():
            if any(datos_terceros_form.cleaned_data.values()):
                datos_terceros = datos_terceros_form.save(commit=False)
                datos_terceros.task = task
                datos_terceros.save()
                return redirect('task_detail_importados', task_id=task_id)
            
        if edificio_verde_form.is_valid():
            if any(edificio_verde_form.cleaned_data.values()):
                edificio_verde = edificio_verde_form.save(commit=False)
                edificio_verde.task = task
                edificio_verde.save()
                return redirect('task_detail_importados', task_id=task_id)
            
        if colindancia_form.is_valid():
             if any(colindancia_form.cleaned_data.values()):
                colindancia = colindancia_form.save(commit=False)
                colindancia.task = task
                colindancia.save()      
                return redirect('task_detail_importados', task_id=task_id)
            
        if tramite_disposicion_form.is_valid():
             if any(tramite_disposicion_form.cleaned_data.values()):
                tramite_disposicion = tramite_disposicion_form.save(commit=False)
                tramite_disposicion.task = task
                tramite_disposicion.save()
                return redirect('task_detail_importados', task_id=task_id)
            
        if edificacion_form.is_valid():
             if any(edificacion_form.cleaned_data.values()):
                edificacion = edificacion_form.save(commit=False)
                edificacion.task = task
                edificacion.save()
                return redirect('task_detail_importados', task_id=task_id)
            
        
        if inmueble.is_valid():
            inmueble.save()  # Guardar los cambios en la tarea
            return redirect('tasks_importados')  # Redireccionar a 'tasks_importados' después de guardar
        
    else:
        inmueble = InmuebleForm(instance=task)
        documento_propiedad_form = DocumentoPropiedadFormIMP()
        datos_avaluos_form = DatosAvaluosFormIMP()
        ocupaciones_form = OcupacionesFormIMP()
        documento_ocupacion_form = DocumentoOcupacionFormIMP()
        instituciones_ocupantes_form = InstitucionesOcupantesFormIMP()
        datos_terceros_form = DatosTercerosFormIMP()
        edificio_verde_form = Edificio_VerdeFormIMP()
        colindancia_form = ColindanciasFormIMP()
        tramite_disposicion_form = TramitesDisposicionFormIMP()
        edificacion_form = EdificacionFormIMP()
        instituciones_ocupantes_form = InstitucionesOcupantesFormIMP()
        mensaje_form = MensajeFormIMP(prefix='mensaje') 
        
    return render(request, 'task_detail_importados.html', {
        'task': task,
        'inmueble': inmueble,
        'edificio_verde_form': edificio_verde_form,
        'edificacion_form': edificacion_form,
        'documento_propiedad_form': documento_propiedad_form,
        'datos_avaluos_form': datos_avaluos_form,
        'ocupaciones_form': ocupaciones_form,
        'documento_ocupacion_form': documento_ocupacion_form,
        'instituciones_ocupantes_form': instituciones_ocupantes_form,
        'datos_terceros_form': datos_terceros_form,
        'colindancia_form': colindancia_form,
        'tramite_disposicion_form': tramite_disposicion_form,
        'mensaje_form': mensaje_form,
    })
    
@login_required
def completar_mensajeIMP(request, mensaje_id):
    if request.method == 'POST':
        mensaje = MensajeIMP.objects.get(id=mensaje_id)
        mensaje.estado = 'completado'
        mensaje.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


from django.shortcuts import render, get_object_or_404, redirect
from .models import FoliosRealesIMP
from .forms import FoliosRealesFormIMP

from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def agregar_dictamen_estructural(request, task_id):
    inmueble = get_object_or_404(Inmueble, pk=task_id)

    if request.method == 'POST':
        dictamen_estructural_form = DictamenEstructuralForm(request.POST, request.FILES)

        if not request.POST.get('no_de_identificador_del_expediente_institucion', '').strip():
            error_message = 'Todos los campos son requeridos.'
            return JsonResponse({'success': False, 'error_message': error_message}, status=400)

        if dictamen_estructural_form.is_valid():
            dictamen_estructural = dictamen_estructural_form.save(commit=False)
            dictamen_estructural.task = inmueble
            dictamen_estructural.save()
            return JsonResponse({'success': True, 'message': 'Dictamen Estructural agregado correctamente.'})
        else:
            # Manejar errores de formulario
            error_message = 'Ya existe un Dictamen Estructural con este ID'
            errors = dictamen_estructural_form.errors.as_json()
            return JsonResponse({'success': False, 'error_message': error_message, 'errors': errors}, status=400)
    else:
        dictamen_estructural_form = DictamenEstructuralForm()

    return render(request, 'add/add_dictamen.html', {'inmueble': inmueble, 'dictamen_estructural_form': dictamen_estructural_form})


@login_required
def agregar_folio_real(request, task_id):
    inmueble = get_object_or_404(Inmueble, pk=task_id)
    if request.method == 'POST':
        folio_real_form = FoliosRealesFormIMP(request.POST, request.FILES)

# Validar si el campo está vacío y devolver un error
        if not request.POST.get('folios_reales_data', '').strip():
            error_message = 'El campo Folio real es requerido'
            return JsonResponse({'success': False, 'error_message': error_message}, status=400)


        if folio_real_form.is_valid():
            folio_real = folio_real_form.save(commit=False)
            folio_real.task = inmueble
            folio_real.save()
            return JsonResponse({'success': True, 'message': 'Folio Real agregado correctamente.'})
        else:
            # Manejar errores de formulario
            error_message = 'Ya existe un Folio Real con este ID'
            errors = folio_real_form.errors.as_json()
            return JsonResponse({'success': False, 'error_message': error_message, 'errors': errors}, status=400)
    else:
        folio_real_form = FoliosRealesFormIMP()
    return render(request, 'add/add_folios_reales.html', {'inmueble': inmueble, 'folio_real_form': folio_real_form})

@login_required
def agregar_no_plano(request, task_id):
    inmueble = get_object_or_404(Inmueble, pk=task_id)
    if request.method == 'POST':
        numero_plano_form = Numero_PlanoFormIMP(request.POST, request.FILES)

                # Validar si el campo está vacío y devolver un error
        if not request.POST.get('numero_plano_data', '').strip():
            error_message = 'El campo número plano es requerido.'
            return JsonResponse({'success': False, 'error_message': error_message}, status=400)
        
        if numero_plano_form.is_valid():
            numero_plano = numero_plano_form.save(commit=False)
            numero_plano.task = inmueble
            numero_plano.save()
            return JsonResponse({'success': True, 'message': 'Numero plano  agregado correctamente.'})
        else:
            # Manejar errores de formulario
            error_message = 'Ya existe un número plano con este ID'
            errors = numero_plano_form.errors.as_json()
            return JsonResponse({'success': False, 'error_message': error_message, 'errors': errors}, status=400)
    else:
        numero_plano_form = Numero_PlanoFormIMP()
    return render(request, 'add/add_NoPlano.html', {'inmueble': inmueble, 'numero_plano_form': numero_plano_form})

from django.http import JsonResponse

@login_required
def agregar_expediente_CEDOC(request, task_id):
    inmueble = get_object_or_404(Inmueble, pk=task_id)

    if request.method == 'POST':
        expediente_form = Expedientes_CEDOCFormIMP(request.POST, request.FILES)
        
        # Validar si el campo está vacío y devolver un error
        if not request.POST.get('expediente_cedoc_data', '').strip():
            error_message = 'Este campo expediente CEDOC es requerido.'
            return JsonResponse({'success': False, 'error_message': error_message}, status=400)

        if expediente_form.is_valid():
            expediente = expediente_form.save(commit=False)
            expediente.task = inmueble
            expediente.save()
            return JsonResponse({'success': True, 'message': 'Expediente CEDOC agregado correctamente.'})
        else:
            # Manejar errores de formulario
            error_message = 'Ya existe un expediente CEDOC con este ID'
            errors = expediente_form.errors.as_json()
            return JsonResponse({'success': False, 'error_message': error_message, 'errors': errors}, status=400)

    else:
        expediente_form = Expedientes_CEDOCFormIMP()

    return render(request, 'add/add_expedientes_cedoc.html', {'inmueble': inmueble, 'expediente_form': expediente_form})




def guardar_documento_ocupacionIMP(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    if request.method == 'POST':
        documento_ocupacion_form = DocumentoOcupacionFormIMP(request.POST)

        if documento_ocupacion_form.is_valid():
            # Realiza cualquier validación adicional si es necesario
            documento_ocupacion = documento_ocupacion_form.save(commit=False)
            # Asegúrate de obtener la tarea relacionada correctamente
            documento_ocupacion.task = task
            documento_ocupacion.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": False})


def guardar_instituciones_ocupantesIMP(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    if request.method == 'POST':
        instituciones_ocupantes_form = InstitucionesOcupantesFormIMP(request.POST)

        if instituciones_ocupantes_form.is_valid():
            # Realiza cualquier validación adicional si es necesario
            instituciones_ocupantes = instituciones_ocupantes_form.save(commit=False)
            # Asegúrate de obtener la tarea relacionada correctamente
            instituciones_ocupantes.task = task
            instituciones_ocupantes.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": False})


def guardar_datos_tercerosIMP(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    if request.method == 'POST':
        datos_terceros_form = DatosTercerosFormIMP(request.POST)

        if datos_terceros_form.is_valid():
            # Realiza cualquier validación adicional si es necesario
            datos_terceros = datos_terceros_form.save(commit=False)
            # Asegúrate de obtener la tarea relacionada correctamente
            datos_terceros.task = task
            datos_terceros.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": False})
    

def guardar_docPropiedadIMP(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    if request.method == 'POST':
        documento_propiedad_form = DocumentoPropiedadFormIMP(request.POST, request.FILES)

        if documento_propiedad_form.is_valid():
            # Realiza cualquier validación adicional si es necesario
            documento_propiedad = documento_propiedad_form.save(commit=False)
            # Asegúrate de obtener la tarea relacionada correctamente
            documento_propiedad.task = task
            documento_propiedad.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": False})


def guardar_AvaluoIMP(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    if request.method == 'POST':
        datos_avaluos_form = DatosAvaluosFormIMP(request.POST)

        if datos_avaluos_form.is_valid():
            # Realiza cualquier validación adicional si es necesario
            datos_avaluo = datos_avaluos_form.save(commit=False)
            # Asegúrate de obtener la tarea relacionada correctamente
            datos_avaluo.task = task
            datos_avaluo.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": False})



def guardar_OcupacionesIMP(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    if request.method == 'POST':
        ocupaciones_form = OcupacionesFormIMP(request.POST)

        if ocupaciones_form.is_valid():
            # Realiza cualquier validación adicional si es necesario
            ocupaciones = ocupaciones_form.save(commit=False)
            # Asegúrate de obtener la tarea relacionada correctamente
            ocupaciones.task = task
            ocupaciones.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": False})
                
               
# Eliminar folios
def delete_folio_realIMP(request, task_id, folio_real_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    folio_real = get_object_or_404(FoliosRealesIMP, pk=folio_real_id, task=task)
    
    # Eliminar el folio real
    folio_real.delete()
    
    # Devolver una respuesta JSON indicando que la eliminación fue exitosa
    return JsonResponse({'success': True})


def delete_numero_planoIMP(request, task_id, numero_plano_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    numero_plano = get_object_or_404(NumeroPlanoIMP, pk=numero_plano_id, task=task)

    # Eliminar el número de plano
    numero_plano.delete()

    # Devolver una respuesta JSON indicando que la eliminación fue exitosa
    return JsonResponse({'success': True})



def delete_expediente_cedocIMP(request, task_id, expediente_cedoc_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    expediente_cedoc = get_object_or_404(Expedientes_CEDOCIMP, pk=expediente_cedoc_id, task=task)

    # Eliminar el expediente cedoc
    expediente_cedoc.delete()

    # Devolver una respuesta JSON indicando que la eliminación fue exitosa
    return JsonResponse({'success': True})

def delete_edificio_verdeIMP(request, task_id, edificio_verde_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    edificio_verde = get_object_or_404(EdificioVerdeIMP, pk=edificio_verde_id, task=task)
    edificio_verde.delete()
    return JsonResponse({'success': True})

def delete_ColindanciaIMP(request, task_id, colindancia_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    colindancia = get_object_or_404(ColindanciasIMP, pk=colindancia_id, task=task)
    colindancia.delete()
    return JsonResponse({'success': True})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
class TaskDeleteView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Inmueble, id=task_id)
        form = PasswordConfirmationForm()
        return render(request, 'delete_task.html', {'task': task, 'form': form})

    def post(self, request, task_id):
        task = get_object_or_404(Inmueble, id=task_id)
        form = PasswordConfirmationForm(request.POST)
        
        if form.is_valid():
            # Validar la contraseña del usuario aquí
            password = form.cleaned_data['password']
            
            # Lógica para validar la contraseña
            # En este ejemplo, suponemos que tienes un usuario autenticado en request.user
            if request.user.check_password(password):
                # Si la contraseña es válida, eliminar la tarea y redirigir a la lista de tareas
                task.delete()
                return redirect('tasks')
            else:
                # Si la contraseña no es válida, mostrar un mensaje de error
                form.add_error('password', 'Contraseña incorrecta. Inténtalo de nuevo.')

        return render(request, 'delete_task.html', {'task': task, 'form': form})

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

    
@login_required
def editar_edificacionIMP(request, edificacion_id):
    edificacion = get_object_or_404(EdificacionIMP, pk=edificacion_id)

    if request.method == 'POST':
        inmueble = EdificacionFormIMP(request.POST, instance=edificacion)
        if inmueble.is_valid():
            inmueble.save()
            return redirect('task_detail_importados', task_id=edificacion.task.id)
    else:
        inmueble = EdificacionFormIMP(instance=edificacion)

    return render(request, 'update/editar_edificacion_imp.html', {
        'inmueble': inmueble,
        'edificacion': edificacion,
    })

@login_required
def borrar_edificacionIMP(request, edificacion_id):
    edificacion = get_object_or_404(EdificacionIMP, pk=edificacion_id)
    task_id = edificacion.task_id
    edificacion.delete()
    return redirect('task_detail_importados', task_id=task_id)


# Edicion Titulo De Propiedad
@login_required
def editar_documentoIMP(request, documento_id):
    documento = get_object_or_404(DocumentoPropiedadIMP, id=documento_id)
    if request.method == 'POST':
        form = DocumentoPropiedadFormIMP(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            return redirect('task_detail_importados', task_id=documento.task_id)
    else:
        form = DocumentoPropiedadFormIMP(instance=documento)
    return render(request, 'update/editar_documentoIMP.html', {'form': form, 'documento': documento})


def eliminar_documentoIMP(request, documento_id):
    documento = get_object_or_404(DocumentoPropiedadIMP, id=documento_id)
    task_id = documento.task_id
    documento.delete()
    return redirect('task_detail_importados', task_id=task_id)

# Edicion avaluo
@login_required
def editar_avaluoIMP(request, avaluo_id):
    avaluo = get_object_or_404(DatosAvaluosIMP, id=avaluo_id)

    if request.method == 'POST':
        form = DatosAvaluosFormIMP(request.POST, instance=avaluo)
        if form.is_valid():
            form.save()
            return redirect('task_detail_importados', task_id=avaluo.task_id)  # Redirige a la página de detalle de la tarea
    else:
        form = DatosAvaluosFormIMP(instance=avaluo)

    return render(request, 'update/editar_avaluoIMP.html', {
        'avaluo': avaluo,
        'form': form,
    })
    
@login_required
def eliminar_avaluoIMP(request, avaluo_id):
    avaluo = get_object_or_404(DatosAvaluosIMP, pk=avaluo_id)
    task_id = avaluo.task_id
    avaluo.delete()
    return redirect('task_detail_importados', task_id=task_id)


@login_required
def editar_ocupacionIMP(request, ocupacion_id):
    ocupacion = get_object_or_404(OcupacionesIMP, id=ocupacion_id)

    if request.method == 'POST':
        form = OcupacionesFormIMP(request.POST, instance=ocupacion)
        if form.is_valid():
            form.save()
            return redirect('task_detail_importados', task_id=ocupacion.task_id)  # Redirige a la página de detalle de la tarea
    else:
        form = OcupacionesFormIMP(instance=ocupacion)

    return render(request, 'update/editar_ocupacionIMP.html', {
        'ocupacion': ocupacion,
        'form': form,
    })

@login_required
def eliminar_ocupacionIMP(request, ocupacion_id):
    ocupacion = get_object_or_404(OcupacionesIMP, pk=ocupacion_id)
    task_id = ocupacion.task_id
    ocupacion.delete()
    return redirect('task_detail_importados', task_id=task_id)


@login_required
def eliminar_tramite(request, tramite_id):
    tramite = get_object_or_404(TramitesDisposicionIMP, pk=tramite_id)
    task_id = tramite.task_id
    tramite.delete()
    return redirect('task_detail_importados', task_id=task_id)


from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def eliminar_dictamenIMP(request, dictamen_estructural_id):
    dictamen_estructural = get_object_or_404(DictamenEstructuralIMP, pk=dictamen_estructural_id)
    task_id = dictamen_estructural.task_id
    dictamen_estructural.delete()
    return redirect('task_detail_importados', task_id=task_id)


def eliminar_docOcupacionIMP(request, docOcupacion_id):
    docOcupacion = get_object_or_404(Documento_ocupacionIMP, pk=docOcupacion_id)
    task_id = docOcupacion.task_id
    docOcupacion.delete()
    return redirect('task_detail_importados', task_id=task_id)


def eliminar_DatoInstitucionOcupanteIMP(request, datoInstitucionOcupante_id):
    datoInstitucionOcupante = get_object_or_404(InstitucionesOcupantesIMP, pk=datoInstitucionOcupante_id)
    task_id = datoInstitucionOcupante.task_id
    datoInstitucionOcupante.delete()
    return redirect('task_detail_importados', task_id=task_id)


def deleteDatosTercerosIMP(request, datos_terceros_id):
    datos_terceros = get_object_or_404(DatosTercerosIMP, pk=datos_terceros_id)
    task_id = datos_terceros.task_id
    datos_terceros.delete()
    return redirect('task_detail_importados', task_id=task_id)



from django.shortcuts import get_object_or_404, render
from .utils import render_to_pdf
from django.http import HttpResponse

@login_required
def generate_pdfIMP(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)

    context = {
        'task': task,
        'STATIC_URL': settings.STATIC_URL
    }

    pdf = render_to_pdf('pdf_template.html', context)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"task_{task_id}.pdf"
        content = f"inline; filename={filename}"
        response['Content-Disposition'] = content
        return response

    return HttpResponse("Error al generar el PDF.", status=500)


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



from tasks.resource import InmuebleResource

from tablib import Dataset 
 
from django.http import HttpResponse
from django.shortcuts import render
from tablib import Dataset


from tablib import Dataset
from django.contrib import messages
@login_required
def importar(request):
    if request.method == 'POST':
        inmueble_resource = InmuebleResource()
        dataset = Dataset()
        
        archivo = request.FILES['archivo']

        if archivo.name.endswith('.csv'):
            imported_data = dataset.load(archivo.read().decode('utf-8'), format='csv')
        elif archivo.name.endswith(('xls', 'xlsx')):
            imported_data = dataset.load(archivo.read(), format='xlsx')
        else:
            messages.error(request, 'El archivo no es ni un archivo CSV ni un archivo Excel válido.')
            return render(request, 'importar.html')

        result = inmueble_resource.import_data(dataset, dry_run=True)
        
        if not result.has_errors():
            # Realiza la importación real
            result = inmueble_resource.import_data(dataset, dry_run=False)
            messages.success(request, 'Los datos se importaron con éxito.')
        else:
            messages.error(request, 'Se encontraron errores en la importación.')

    return render(request, 'importar.html')


