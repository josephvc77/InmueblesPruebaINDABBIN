
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

from .forms import BajaForm, ColindanciasForm, ColindanciasFormIMP, DatosAvaluosForm, DatosAvaluosFormIMP, DatosTercerosForm, DatosTercerosFormIMP, DocumentoOcupacionForm, DocumentoOcupacionFormIMP, DocumentoPropiedadForm, DocumentoPropiedadFormIMP, EdificacionForm, EdificacionFormIMP, Edificio_VerdeForm, Edificio_VerdeFormIMP, Expedientes_CEDOCFormIMP, FoliosRealesFormIMP, InmuebleForm, InstitucionesOcupantesForm, InstitucionesOcupantesFormIMP, Numero_PlanoFormIMP, OcupacionesForm, OcupacionesFormIMP, PasswordConfirmationForm, TramitesDisposicionForm, TramitesDisposicionFormIMP
from .models import Colindancias, DatosAvaluos, DatosAvaluosIMP, DatosTerceros, DatosTercerosIMP, Documento_ocupacion, Documento_ocupacionIMP, DocumentoPropiedad, DocumentoPropiedadIMP, Edificacion, EdificacionIMP, EdificioVerde, EdificioVerdeIMP, Expedientes_CEDOC, Expedientes_CEDOCIMP, FoliosReales, FoliosRealesIMP, Inmueble, InstitucionesOcupantes, InstitucionesOcupantesIMP, NumeroPlano, NumeroPlanoIMP, Ocupaciones, OcupacionesIMP, Task, TramitesDisposicion

from .forms import Expedientes_CEDOCForm, FoliosRealesForm, Numero_PlanoForm, TaskCreateForm, TaskForm

# Create your views here.

# Vista para cerrar sesión automáticamente
from django.contrib.auth import logout

class AutoLogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('home')

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


@login_required
def tasks(request):
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')  # Obtén el valor de prioridad desde la solicitud GET

    inmuebles = Inmueble.objects.all()

    tasks = Task.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        user=request.user,
        datecompleted__isnull=True,
        estado='Activo'  # Filtra las tareas en estado 'Activo'
    )

    if prioridad:
        tasks = tasks.filter(prioridad=prioridad)  # Filtra las tareas por prioridad si se ha seleccionado una
        
    paginator = Paginator(inmuebles, 20)  # Muestra 20 inmuebles por página

    page = request.GET.get('page')
    try:
        inmuebles = paginator.page(page)
    except PageNotAnInteger:
        inmuebles = paginator.page(1)
    except EmptyPage:
        inmuebles = paginator.page(paginator.num_pages)

    total_pending_tasks = tasks.count()  # Total de tareas pendientes por completar
    total_completed_tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).count()  # Total de tareas completadas

    return render(request, 'tasks.html', {
        'tasks': tasks,
        'search_query': search_query,
        'total_pending_tasks': total_pending_tasks,
        'total_completed_tasks': total_completed_tasks,
        'inmuebles': inmuebles, 
    })

    
    
from django.db.models import Q
from django.shortcuts import render
from .models import Inmueble

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from .models import Inmueble

@login_required
def tasks_importados(request):
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')

    inmuebles_list = Inmueble.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        datecompleted__isnull=True,
        estado='Activo'  # Filtra las tareas en estado 'Activo'
    ).order_by('NombreInmueble')

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
    })



@login_required
def principal(request):
    return render(request, 'tasks.html')

@login_required
def tasks_completed(request):
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')  # Obtén el valor de prioridad desde la solicitud GET

    tasks = Task.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        user=request.user,
        datecompleted__isnull=False
    ).order_by('-datecompleted')

    if prioridad:
        tasks = tasks.filter(prioridad=prioridad)  # Filtra las tareas completadas por prioridad si se ha seleccionado una

    total_pending_tasks = Task.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        user=request.user,
        datecompleted__isnull=True
    ).count()  # Total de tareas pendientes por completar
    
    paginator = Paginator(tasks, 20)  # Muestra 20 tasks por página

    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    total_completed_tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).count()  # Total de tareas completadas

    return render(request, 'tasks.html', {
        'tasks': tasks,
        'search_query': search_query,
        'total_pending_tasks': total_pending_tasks,
        'total_completed_tasks': total_completed_tasks,
    })
    

@login_required
def inmuebles_baja(request):
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')

    tasks = Task.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        user=request.user,
        estado='Baja'  # Filtra las tareas con estado 'Baja'
    ).order_by('-datecompleted')

    if prioridad:
        tasks = tasks.filter(prioridad=prioridad)

    total_pending_tasks = Task.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        user=request.user,
        datecompleted__isnull=True
    ).count()  # Total de tareas pendientes por completar
    
    paginator = Paginator(tasks, 20)  # Muestra 20 tasks por página

    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    total_completed_tasks = Task.objects.filter(user=request.user, estado='Baja').count()  # Total de tareas en estado 'Baja'

    return render(request, 'tasks.html', {
        'tasks': tasks,
        'search_query': search_query,
        'total_pending_tasks': total_pending_tasks,
        'total_completed_tasks': total_completed_tasks,
    })



@login_required
def inmuebles_baja_importados(request):
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')

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
    })


@login_required
def tasks_completed_importados(request):
    search_query = request.GET.get('q', '')
    prioridad = request.GET.get('prioridad', '')

    inmuebles_list = Inmueble.objects.filter(
        Q(NombreInmueble__icontains=search_query) |
        Q(rfi__icontains=search_query) |
        Q(municipio_alcaldia__icontains=search_query) |
        Q(entidad_federativa__icontains=search_query),
        datecompleted__isnull=False
        
    ).order_by('-datecompleted')

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

    total_completed_inmuebles = Inmueble.objects.filter(datecompleted__isnull=False).count()  # Total de inmuebles completados

    return render(request, 'importados.html', {
        'inmuebles': inmuebles,
        'search_query': search_query,
        'total_pending_inmuebles': total_pending_inmuebles,
        'total_completed_inmuebles': total_completed_inmuebles,
    })
    
    
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def bajas(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if task.estado == 'Activo':
        if request.method == 'POST':
            form = BajaForm(request.POST)
            if form.is_valid():
                task.estado = 'Baja'
                task.save()
                return redirect('inmuebles_baja')
        else:
            form = BajaForm()


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


def complete_task_importados(request, task_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks_importados')



@login_required
def dar_de_baja_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if task.estado == 'Activo':
        if request.method == 'POST':
            # Procesar el formulario de dar de baja
            form = BajaForm(request.POST)
            if form.is_valid():
                task.estado = 'Baja'
                task.save()
                return redirect('task_detail', task_id=task_id)
        else:
            # Mostrar el formulario para dar de baja
            form = BajaForm()

        return render(request, 'baja.html', {'task': task, 'form': form})

    return redirect('tasks')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Mensaje
from .forms import MensajeForm





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
            return redirect('tasks')
    else:
        form = TaskCreateForm(user=request.user)
    context = {'form': form}
    return render(request, 'create_task.html', context)



@login_required
def signout(request):
    logout(request)
    return redirect('signin')


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks')
    else:
        form = AuthenticationForm()
    
    return render(request, 'signin.html', {"form": form})
    
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    
    inscripcion_rppf_exists = task.documentopropiedad_set.filter(inscripcion_rppf='Si').exists()
    inscripcion_registro_local_exists = task.documentopropiedad_set.filter(inscripcion_registro_local='Si').exists()
    
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        edificio_verde_form = Edificio_VerdeForm(request.POST)
        documento_propiedad_form = DocumentoPropiedadForm(request.POST, request.FILES)
        datos_avaluos_form = DatosAvaluosForm(request.POST)
        ocupaciones_form = OcupacionesForm(request.POST)
        documento_ocupacion_form = DocumentoOcupacionForm(request.POST)
        instituciones_ocupantes_form = InstitucionesOcupantesForm(request.POST)
        datos_terceros_form = DatosTercerosForm(request.POST)
        colindancia_form = ColindanciasForm(request.POST)
        tramite_disposicion_form = TramitesDisposicionForm(request.POST)
        folios_reales_data_form = FoliosRealesForm(request.POST)
        numero_plano_data_form = Numero_PlanoForm(request.POST)
        expediente_cedoc_data_form = Expedientes_CEDOCForm(request.POST)
        edificacion_form = EdificacionForm(request.POST)
        baja_form = BajaForm(request.POST)
        mensaje_form = MensajeForm(request.POST)
        
        
        if documento_propiedad_form.is_valid():
            # Validación adicional para verificar si hay datos antes de guardar
            if any(documento_propiedad_form.cleaned_data.values()):
                documento_propiedad = documento_propiedad_form.save(commit=False)
                documento_propiedad.task = task
                documento_propiedad.save()
                return redirect('task_detail', task_id=task_id)
        
        if datos_avaluos_form.is_valid():
            if any(datos_avaluos_form.cleaned_data.values()):
                datos_avaluo = datos_avaluos_form.save(commit=False)
                datos_avaluo.task = task
                datos_avaluo.save()
                return redirect('task_detail', task_id=task_id)
            
        if folios_reales_data_form.is_valid():
            if any(folios_reales_data_form.cleaned_data.values()):
                # Obtener el folio real del formulario
                folio_real = folios_reales_data_form.cleaned_data['folios_reales_data']

                # Verificar si el folio real ya existe en la base de datos
                folio_real_existente = FoliosReales.objects.filter(task=task, folios_reales_data=folio_real).exists()

                if not folio_real_existente:
                    # El folio real no existe, guardar el formulario
                    folios_reales_data = folios_reales_data_form.save(commit=False)
                    folios_reales_data.task = task
                    folios_reales_data.save()
                    return redirect('task_detail', task_id=task_id)
                else:
                    # El folio real ya existe, mostrar una alerta
                    messages.error(request, 'El folio real ya existe en esta tarea.')
            else:
                print(f"Form errors: {folios_reales_data_form.errors}")
            
        if numero_plano_data_form.is_valid():
            if any(numero_plano_data_form.cleaned_data.values()):
                numero_plano_data = numero_plano_data_form.save(commit=False)
                numero_plano_data.task = task
                numero_plano_data.save()
                return redirect('task_detail', task_id=task_id)
            
        if expediente_cedoc_data_form.is_valid():
            if any(expediente_cedoc_data_form.cleaned_data.values()):
                expediente_cedoc_data = expediente_cedoc_data_form.save(commit=False)
                expediente_cedoc_data.task = task
                expediente_cedoc_data.save()
                return redirect('task_detail', task_id=task_id)
        
        if ocupaciones_form.is_valid():
            if any(ocupaciones_form.cleaned_data.values()):
                ocupaciones = ocupaciones_form.save(commit=False)
                ocupaciones.task = task
                ocupaciones.save()
                return redirect('task_detail', task_id=task_id)
            
        if mensaje_form.is_valid():
            mensaje_form.instance.enviado_por = request.user
            if any(mensaje_form.cleaned_data.values()):
                mensaje = mensaje_form.save(commit=False)
                mensaje.task = task
                mensaje.save()
                return redirect('tasks',)
            
        if documento_ocupacion_form.is_valid():
            if any(documento_ocupacion_form.cleaned_data.values()):
                documento_ocupacion = documento_ocupacion_form.save(commit=False)
                documento_ocupacion.task = task
                documento_ocupacion.save()
                return redirect('task_detail', task_id=task_id)
            
        if instituciones_ocupantes_form.is_valid():
            if any(instituciones_ocupantes_form.cleaned_data.values()):
                instituciones_ocupantes = instituciones_ocupantes_form.save(commit=False)
                instituciones_ocupantes.task = task
                instituciones_ocupantes.save()
                return redirect('task_detail', task_id=task_id)
        
        if datos_terceros_form.is_valid():
            if any(datos_terceros_form.cleaned_data.values()):
                datos_terceros = datos_terceros_form.save(commit=False)
                datos_terceros.task = task
                datos_terceros.save()
                return redirect('task_detail', task_id=task_id)
            
        if edificio_verde_form.is_valid():
            if any(edificio_verde_form.cleaned_data.values()):
                edificio_verde = edificio_verde_form.save(commit=False)
                edificio_verde.task = task
                edificio_verde.save()
                return redirect('task_detail', task_id=task_id)
            
        if colindancia_form.is_valid():
             if any(colindancia_form.cleaned_data.values()):
                colindancia = colindancia_form.save(commit=False)
                colindancia.task = task
                colindancia.save()      
                return redirect('task_detail', task_id=task_id)
            
        if tramite_disposicion_form.is_valid():
             if any(tramite_disposicion_form.cleaned_data.values()):
                tramite_disposicion = tramite_disposicion_form.save(commit=False)
                tramite_disposicion.task = task
                tramite_disposicion.save()
                return redirect('task_detail', task_id=task_id)
            
        if edificacion_form.is_valid():
             if any(edificacion_form.cleaned_data.values()):
                edificacion = edificacion_form.save(commit=False)
                edificacion.task = task
                edificacion.save()
                return redirect('task_detail', task_id=task_id)
            
        if baja_form.is_valid():
            if any(baja_form.cleaned_data.values()):
                baja = baja_form.save(commit=False)
                baja.task = task
                baja.save()
                return redirect('task_detail', task_id=task_id)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
        
    else:
        form = TaskForm(instance=task)
        documento_propiedad_form = DocumentoPropiedadForm()
        datos_avaluos_form = DatosAvaluosForm()
        ocupaciones_form = OcupacionesForm()
        documento_ocupacion_form = DocumentoOcupacionForm()
        instituciones_ocupantes_form = InstitucionesOcupantesForm()
        datos_terceros_form = DatosTercerosForm()
        edificio_verde_form = Edificio_VerdeForm()
        colindancia_form = ColindanciasForm()
        tramite_disposicion_form = TramitesDisposicionForm()
        folios_reales_data_form = FoliosRealesForm()
        numero_plano_data_form = Numero_PlanoForm()
        expediente_cedoc_data_form = Expedientes_CEDOCForm()
        edificacion_form = EdificacionForm()
        instituciones_ocupantes_form = InstitucionesOcupantesForm()
        baja_form = BajaForm()
        mensaje_form = MensajeForm(request.POST)


    return render(request, 'task_detail.html', {
        'task': task,
        'form': form,
        'folios_reales_data_form': folios_reales_data_form,
        'edificio_verde_form': edificio_verde_form,
        'edificacion_form': edificacion_form,
        'documento_propiedad_form': documento_propiedad_form,
        'datos_avaluos_form': datos_avaluos_form,
        'ocupaciones_form': ocupaciones_form,
        'inscripcion_rppf_exists': inscripcion_rppf_exists,
        'inscripcion_registro_local_exists': inscripcion_registro_local_exists,
        'documento_ocupacion_form': documento_ocupacion_form,
        'instituciones_ocupantes_form': instituciones_ocupantes_form,
        'datos_terceros_form': datos_terceros_form,
        'colindancia_form': colindancia_form,
        'tramite_disposicion_form': tramite_disposicion_form,
        'numero_plano_data_form': numero_plano_data_form,
        'expediente_cedoc_data_form': expediente_cedoc_data_form,
        'baja_form': baja_form,
        'mensaje_form': mensaje_form
        
    })



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
        folios_reales_data_form = FoliosRealesFormIMP(request.POST)
        numero_plano_data_form = Numero_PlanoFormIMP(request.POST)
        expediente_cedoc_data_form = Expedientes_CEDOCFormIMP(request.POST)
        edificacion_form = EdificacionFormIMP(request.POST)
        
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
            
        if folios_reales_data_form.is_valid():
            if any(folios_reales_data_form.cleaned_data.values()):
                # Obtener el folio real del formulario
                folio_real = folios_reales_data_form.cleaned_data['folios_reales_data']

                # Verificar si el folio real ya existe en la base de datos
                folio_real_existente = FoliosRealesIMP.objects.filter(task=task, folios_reales_data=folio_real).exists()

                if not folio_real_existente:
                    # El folio real no existe, guardar el formulario
                    folios_reales_data = folios_reales_data_form.save(commit=False)
                    folios_reales_data.task = task
                    folios_reales_data.save()
                    return redirect('task_detail_importados', task_id=task_id)
                else:
                    # El folio real ya existe, mostrar una alerta
                    messages.error(request, 'El folio real ya existe en esta tarea.')
            else:
                print(f"Form errors: {folios_reales_data_form.errors}")
            
        if numero_plano_data_form.is_valid():
            if any(numero_plano_data_form.cleaned_data.values()):
                numero_plano_data = numero_plano_data_form.save(commit=False)
                numero_plano_data.task = task
                numero_plano_data.save()
                return redirect('task_detail_importados', task_id=task_id)
            
        if expediente_cedoc_data_form.is_valid():
            if any(expediente_cedoc_data_form.cleaned_data.values()):
                expediente_cedoc_data = expediente_cedoc_data_form.save(commit=False)
                expediente_cedoc_data.task = task
                expediente_cedoc_data.save()
                return redirect('task_detail_importados', task_id=task_id)
        
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
        folios_reales_data_form = FoliosRealesFormIMP()
        numero_plano_data_form = Numero_PlanoFormIMP()
        expediente_cedoc_data_form = Expedientes_CEDOCFormIMP()
        edificacion_form = EdificacionFormIMP()
        instituciones_ocupantes_form = InstitucionesOcupantesForm()
        
    return render(request, 'task_detail_importados.html', {
        'task': task,
        'inmueble': inmueble,
        'folios_reales_data_form': folios_reales_data_form,
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
        'numero_plano_data_form': numero_plano_data_form,
        'expediente_cedoc_data_form': expediente_cedoc_data_form,
    })

        

@login_required
def guardar_documento_ocupacion(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        documento_ocupacion_form = DocumentoOcupacionForm(request.POST)

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

@login_required
def guardar_instituciones_ocupantes(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        instituciones_ocupantes_form = InstitucionesOcupantesForm(request.POST)

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


@login_required
def guardar_datos_terceros(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        datos_terceros_form = DatosTercerosForm(request.POST)

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
    
@login_required
def guardar_docPropiedad(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        documento_propiedad_form = DocumentoPropiedadForm(request.POST, request.FILES)

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


@login_required
def guardar_Avaluo(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        datos_avaluos_form = DatosAvaluosForm(request.POST)

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
    
@login_required
def guardar_Ocupaciones(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        ocupaciones_form = OcupacionesForm(request.POST)

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
def delete_folio_real(request, task_id, folio_real_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    folio_real = get_object_or_404(FoliosReales, pk=folio_real_id, task=task)
    
    # Eliminar el folio real
    folio_real.delete()
    
    # Devolver una respuesta JSON indicando que la eliminación fue exitosa
    return JsonResponse({'success': True})


@login_required
def delete_numero_plano(request, task_id, numero_plano_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    numero_plano = get_object_or_404(NumeroPlano, pk=numero_plano_id, task=task)

    # Eliminar el número de plano
    numero_plano.delete()

    # Devolver una respuesta JSON indicando que la eliminación fue exitosa
    return JsonResponse({'success': True})


@login_required
def delete_expediente_cedoc(request, task_id, expediente_cedoc_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    expediente_cedoc = get_object_or_404(Expedientes_CEDOC, pk=expediente_cedoc_id, task=task)

    # Eliminar el expediente cedoc
    expediente_cedoc.delete()

    # Devolver una respuesta JSON indicando que la eliminación fue exitosa
    return JsonResponse({'success': True})


               
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

@login_required
def delete_edificio_verde(request, task_id, edificio_verde_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    edificio_verde = get_object_or_404(EdificioVerde, pk=edificio_verde_id, task=task)
    edificio_verde.delete()
    return JsonResponse({'success': True})


def delete_edificio_verdeIMP(request, task_id, edificio_verde_id):
    task = get_object_or_404(Inmueble, pk=task_id)
    edificio_verde = get_object_or_404(EdificioVerdeIMP, pk=edificio_verde_id, task=task)
    edificio_verde.delete()
    return JsonResponse({'success': True})

@login_required
def delete_tramite(request, task_id, tramite_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    tramite = get_object_or_404(TramitesDisposicion, pk=tramite_id, task=task)
    tramite.delete()
    return JsonResponse({'success': True})

# @login_required
# def delete_tramite(request, tramite_id):
#     tramite = get_object_or_404(TramitesDisposicion, pk=tramite_id)
#     task_id = tramite.task_id
#     tramite.delete()
#     return redirect('task_detail', task_id=task_id)



@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
class TaskDeleteView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = PasswordConfirmationForm()
        return render(request, 'delete_task.html', {'task': task, 'form': form})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
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
def editar_edificacion(request, edificacion_id):
    edificacion = get_object_or_404(Edificacion, pk=edificacion_id)

    if request.method == 'POST':
        form = EdificacionForm(request.POST, instance=edificacion)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=edificacion.task.id)
    else:
        form = EdificacionForm(instance=edificacion)

    return render(request, 'update/editar_edificacion.html', {
        'form': form,
        'edificacion': edificacion,
    })
    
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
def borrar_edificacion(request, edificacion_id):
    edificacion = get_object_or_404(Edificacion, pk=edificacion_id)
    
    if request.method == 'POST':
        edificacion.delete()
        return redirect('task_detail', task_id=edificacion.task.id)
    
    return render(request, 'borrar_edificacion.html', {
        'edificacion': edificacion,
    })
    
@login_required
def borrar_edificacionIMP(request, edificacion_id):
    edificacion = get_object_or_404(EdificacionIMP, pk=edificacion_id)
    
    if request.method == 'POST':
        edificacion.delete()
        return redirect('task_detail_importados', task_id=edificacion.task.id)
    
    return render(request, 'borrar_edificacion.html', {
        'edificacion': edificacion,
    })




# Edicion Titulo De Propiedad
@login_required
def editar_documento(request, documento_id):
    documento = get_object_or_404(DocumentoPropiedad, id=documento_id)
    if request.method == 'POST':
        form = DocumentoPropiedadForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=documento.task_id)
    else:
        form = DocumentoPropiedadForm(instance=documento)
    return render(request, 'update/editar_documento.html', {'form': form, 'documento': documento})

@login_required
def eliminar_documento(request, documento_id):
    documento = get_object_or_404(DocumentoPropiedad, id=documento_id)
    task_id = documento.task_id
    documento.delete()
    return redirect('task_detail', task_id=task_id)

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
        form = DocumentoPropiedadForm(instance=documento)
    return render(request, 'update/editar_documentoIMP.html', {'form': form, 'documento': documento})


def eliminar_documentoIMP(request, documento_id):
    documento = get_object_or_404(DocumentoPropiedadIMP, id=documento_id)
    task_id = documento.task_id
    documento.delete()
    return redirect('task_detail_importados', task_id=task_id)

# Edicion avaluo
@login_required
def editar_avaluo(request, avaluo_id):
    avaluo = get_object_or_404(DatosAvaluos, id=avaluo_id)

    if request.method == 'POST':
        form = DatosAvaluosForm(request.POST, instance=avaluo)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=avaluo.task_id)  # Redirige a la página de detalle de la tarea
    else:
        form = DatosAvaluosForm(instance=avaluo)

    return render(request, 'update/editar_avaluo.html', {
        'avaluo': avaluo,
        'form': form,
    })
    
@login_required
def eliminar_avaluo(request, avaluo_id):
    avaluo = get_object_or_404(DatosAvaluos, pk=avaluo_id)
    task_id = avaluo.task_id
    avaluo.delete()
    return redirect('task_detail', task_id=task_id)

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
        form = DatosAvaluosForm(instance=avaluo)

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


# Edicion Ocupacion
@login_required
def editar_ocupacion(request, ocupacion_id):
    ocupacion = get_object_or_404(Ocupaciones, id=ocupacion_id)

    if request.method == 'POST':
        form = OcupacionesForm(request.POST, instance=ocupacion)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=ocupacion.task_id)  # Redirige a la página de detalle de la tarea
    else:
        form = OcupacionesForm(instance=ocupacion)

    return render(request, 'update/editar_ocupacion.html', {
        'ocupacion': ocupacion,
        'form': form,
    })

@login_required
def eliminar_ocupacion(request, ocupacion_id):
    ocupacion = get_object_or_404(Ocupaciones, pk=ocupacion_id)
    task_id = ocupacion.task_id
    ocupacion.delete()
    return redirect('task_detail', task_id=task_id)

@login_required
def editar_ocupacionIMP(request, ocupacion_id):
    ocupacion = get_object_or_404(OcupacionesIMP, id=ocupacion_id)

    if request.method == 'POST':
        form = OcupacionesFormIMP(request.POST, instance=ocupacion)
        if form.is_valid():
            form.save()
            return redirect('task_detail_importados', task_id=ocupacion.task_id)  # Redirige a la página de detalle de la tarea
    else:
        form = OcupacionesForm(instance=ocupacion)

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


from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def eliminar_docOcupacion(request, docOcupacion_id):
    docOcupacion = get_object_or_404(Documento_ocupacion, pk=docOcupacion_id)
    task_id = docOcupacion.task_id
    docOcupacion.delete()
    return redirect('task_detail', task_id=task_id)

@login_required
def eliminar_DatoInstitucionOcupante(request, datoInstitucionOcupante_id):
    datoInstitucionOcupante = get_object_or_404(InstitucionesOcupantes, pk=datoInstitucionOcupante_id)
    task_id = datoInstitucionOcupante.task_id
    datoInstitucionOcupante.delete()
    return redirect('task_detail', task_id=task_id)

@login_required
def deleteDatosTerceros(request, datos_terceros_id):
    datos_terceros = get_object_or_404(DatosTerceros, pk=datos_terceros_id)
    task_id = datos_terceros.task_id
    datos_terceros.delete()
    return redirect('task_detail', task_id=task_id)


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
from .models import Task
from .utils import render_to_pdf
from django.http import HttpResponse

@login_required
def generate_pdf(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

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
from .models import Task  # Asegúrate de importar tu modelo de tareas
from django.db.models import F
from .models import Task, FoliosReales, NumeroPlano

@login_required
def export_tasks_to_excel(request):
    # Obtener todas las tareas del usuario logueado
    tasks = Task.objects.filter(user=request.user)

    # Crear una lista vacía para almacenar los datos de tareas y modelos relacionados
    data = []

    # Recorrer todas las tareas y obtener los datos necesarios
    for task in tasks:
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
        edificaciones = Edificacion.objects.filter(task=task)
        
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
        colindancias = Colindancias.objects.filter(task=task)
        
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
        documento_ocupacion = Documento_ocupacion.objects.filter(task=task)
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
        instituciones_ocupantes = InstitucionesOcupantes.objects.filter(task=task)
        
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
        dato_terceros = DatosTerceros.objects.filter(task=task)
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
        tramites_disposicion = TramitesDisposicion.objects.filter(task=task)
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
        ocupaciones = Ocupaciones.objects.filter(task=task)
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
        datos_avaluos = DatosAvaluos.objects.filter(task=task)
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
        doc_propiedads = DocumentoPropiedad.objects.filter(task=task)
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
        
        

        # Obtener datos de FoliosReales relacionados con la tarea
        folios_reales_data = task.foliosreales_set.values_list('folios_reales_data', flat=True)

        # Obtener datos de NumeroPlano relacionados con la tarea
        numero_plano_data = task.numeros_planos.values_list('numero_plano_data', flat=True)

        # Obtener datos de Expedientes_CEDOC relacionados con la tarea
        expedientes_cedoc_data = task.expedientes_cedoc_set.values_list('expediente_cedoc_data', flat=True)

        edificio_verde_data = task.edificio_verde_set.values_list('edificio_verde_data', flat=True)

        # Combinar todos los datos en un solo diccionario
        task_data.update({
            'folios_reales': ', '.join(folios_reales_data),
            'numero_plano': ', '.join(numero_plano_data),
            'expedientes_cedoc': ', '.join(expedientes_cedoc_data),
            'edificio_verde': ', '.join(edificio_verde_data)
        })

        data.append(task_data)

    # Convertir la lista de datos a un DataFrame de Pandas
    df = pd.DataFrame(data)

    # Crear la respuesta del archivo Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tareas.xlsx"'

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


