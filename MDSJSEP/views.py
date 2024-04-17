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
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('calendar_MDSJ')
    else:
        form = AuthenticationForm()
    
    return render(request, 'signinMDSJ.html', {"form": form})


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
        all_events = EventosCreados.objects.filter(sala=selected_sala)
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
    sala = request.GET.get("sala", None)
    coordina = request.GET.get("coordina", None)
    preside = request.GET.get("preside", None)
    cargo = request.GET.get("cargo", None)
    no_personas = request.GET.get("no_personas", None)
    contacto = request.GET.get("contacto", None)
    servicios = request.GET.get("servicios", None)
    observaciones = request.GET.get("observaciones", None)
    
    event = EventosCreados(title=title, dia=dia, hora_inicio=hora_inicio, hora_finalizacion=hora_finalizacion, prioridad=prioridad, sala=sala, coordina=coordina, preside=preside, cargo=cargo, no_personas=no_personas,
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