from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.core.files.storage import default_storage
from django import forms
import json
import os
from .models import InmuebleCondia
from .forms import InmuebleCondiaForm, InmuebleCondiaEditarForm
from .utils import get_file_fields_by_folder, get_document_statistics

def signupCondia(request):
    if request.method == 'GET':
        return render(request, 'signupCondia.html')
    else:
        if request.POST.get("password1") == request.POST.get("password2"):
            try:
                from tasks.models import CustomUser
                user = CustomUser.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect('homeCondia')
            except IntegrityError:
                return render(request, 'signupCondia.html', {
                    "error": "El usuario ya existe."
                })
        return render(request, 'signupCondia.html', {
            "error": "Las contraseñas no coinciden."
        })


def signinCondia(request):
    if request.method == 'GET':
        return render(request, 'signinCondia.html', {})
    else:
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user is None:
            messages.error(request, 'Usuario o contraseña son incorrectos', extra_tags='login-error')
            return render(request, 'signinCondia.html', {
                'error': 'Usuario o contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('homeCondia')


@login_required
def signout_condia(request):
    logout(request)
    return redirect('signinCondia')


@login_required
def homeCondia(request):
    query = request.GET.get('q', '')
    inmuebles = InmuebleCondia.objects.all().order_by('-fecha_creacion')
    
    if query:
        inmuebles = inmuebles.filter(
            NombreInmueble__icontains=query
        ) | inmuebles.filter(
            descripcion__icontains=query
        ) | inmuebles.filter(
            arrendatario__icontains=query
        )
    
    context = {
        'inmuebles': inmuebles,
        'query': query,
    }
    return render(request, 'homeCondia.html', context)


@login_required
def crear_inmueble_condia(request):
    if request.method == 'POST':
        form = InmuebleCondiaForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.creado_por = request.user
            inmueble.save()
            messages.success(request, 'El inmueble se creó correctamente ✅')
            return redirect('detalle_inmueble_condia', pk=inmueble.pk)
        else:
            messages.error(request, 'Hubo un error al crear el inmueble ❌')
    else:
        form = InmuebleCondiaForm()
    
    return render(request, 'create_inmueble_condia.html', {'form': form})


@login_required
def inmuebles_list_condia(request):
    inmuebles = InmuebleCondia.objects.all().order_by('-fecha_creacion')
    return render(request, 'inmuebles_list_condia.html', {'inmuebles': inmuebles})


@login_required
def detalle_inmueble_condia(request, pk):
    inmueble = get_object_or_404(InmuebleCondia, pk=pk)
    
    # Manejar edición de campos del inmueble
    if request.method == 'POST' and 'editar_inmueble' in request.POST:
        form = InmuebleCondiaEditarForm(request.POST, request.FILES, instance=inmueble)
        if form.is_valid():
            form.save()
            # Determinar qué tipo de actualización se hizo
            files_uploaded = any(request.FILES.get(field) for field in form.fields.keys() if hasattr(form.fields[field], 'widget') and isinstance(form.fields[field].widget, forms.ClearableFileInput))
            if files_uploaded:
                messages.success(request, 'Documentos actualizados correctamente ✅')
            else:
                messages.success(request, 'Inmueble actualizado correctamente ✅')
            return redirect('detalle_inmueble_condia', pk=pk)
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            messages.error(request, f'Error al actualizar el inmueble ❌ {", ".join(error_messages)}')
    else:
        form = InmuebleCondiaEditarForm(instance=inmueble)
    
    # Obtener estadísticas de documentos
    statistics = get_document_statistics(inmueble)
    folders_info = get_file_fields_by_folder()
    
    context = {
        'inmueble': inmueble,
        'form': form,
        'statistics': statistics,
        'folders_info': folders_info,
    }
    return render(request, 'detalle_inmueble_condia.html', context)


@login_required
@require_POST
def eliminar_archivo_condia(request, pk, field_name):
    """
    Vista para eliminar un archivo específico de un inmueble.
    """
    inmueble = get_object_or_404(InmuebleCondia, pk=pk)
    
    # Verificar que el campo existe en el modelo
    if not hasattr(inmueble, field_name):
        return JsonResponse({'success': False, 'error': 'Campo no válido'}, status=400)
    
    # Obtener el campo y eliminar el archivo
    field = getattr(inmueble, field_name)
    
    if field:
        # Eliminar archivo del sistema de archivos
        if default_storage.exists(field.name):
            default_storage.delete(field.name)
        
        # Limpiar el campo en la base de datos
        setattr(inmueble, field_name, None)
        inmueble.save()
        
        messages.success(request, f'Archivo eliminado correctamente ✅')
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No hay archivo para eliminar'}, status=400)


