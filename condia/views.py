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

from condia.models import TareasCondia
from tasks.forms import CondiaForm, CreateTaskCondiaForm
# Create your views here.


def signupCondia(request):
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
    
def signinCondia(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_condia')
    else:
        form = AuthenticationForm()
    
    return render(request, 'signin.html', {"form": form})

@login_required
def signout_condia(request):
    logout(request)
    return redirect('signinCondia')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
def task_condia(request):
    
    tareas = TareasCondia.objects.all()
        
    return render(request, 'home.html', {
        'tareas' : tareas
    })
    

from tasks.forms import CreateTaskCondiaForm  # Asegúrate de importar el formulario desde la aplicación "tasks"

@login_required
def create_task_CONDIA(request):
    if request.method == 'POST':
        form = CreateTaskCondiaForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('task_condia')  
    else:
        form = CreateTaskCondiaForm()
    context = {'form': form}
    return render(request, 'create_task_condia.html', context)



@login_required
def task_detail_condia(request, task_id):
    task = get_object_or_404(TareasCondia, pk=task_id)
    
    if request.method == 'POST':
        form = CondiaForm(request.POST, request.FILES, instance=task)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_condia')
        
    else:
        form = CondiaForm(instance=task)
        
    return render(request, 'task_detail_condia.html', {
        'task': task,
        'form': form,
    })