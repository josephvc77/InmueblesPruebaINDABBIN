"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from djangocrud import settings
from tasks import views
from condia import views as views_condia
from MDSJSEP import views as views_MDSJ
from django.utils.text import slugify  # Para crear URLs basadas en texto

app_name = 'tasks'

urlpatterns = [
    path('', views.signin, name='signin'),
    path('403/', views.permission_denied, name='permission_denied'),

    path('users/', views.user_list, name='user_list'),
    path('users/edit/<int:id>/', views.edit_user, name='edit_user'),
    path('users/add/', views.add_user, name='add_user'),


    path('llamadas_inmuebles/', views.llamadas_inmuebles, name='llamadas_inmuebles'),
    path('create_DatosLlamadasInmueble/', views.create_DatosLlamadasInmueble, name='create_DatosLlamadasInmueble'),
    path('create_DatosLlamadasInmueble/', views.create_DatosLlamadasInmueble, name='create_DatosLlamadasInmueble'),

    
    path('admin/', admin.site.urls),
    # path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('Inmueble/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('principal/', views.principal, name='principal'),
    path('get_entidades_federativas/', views.get_entidades_federativas, name='get_entidades_federativas'),
    path('get_municipios/<str:entidad_federativa>/', views.get_municipios_by_entidad_federativa, name='get_municipios'),
    # path('get_secciones_inventario/', views.get_secciones_inventario, name='get_secciones_inventario'),
    # path('get_dependencias_administradoras_by_seccion/<str:seccion_inventario>/', views.get_dependencias_administradoras_by_seccion, name='get_dependencias_administradoras_by_seccion'),
    # path('get_subsecciones_by_dependencia_administradora/<str:seccion_inventario>/<str:dependencia_administradora>/', views.get_subsecciones_by_dependencia_administradora, name='get_subsecciones_by_dependencia_administradora'),
    
    # ///////////////////////////////////////////////////////////////////////////////////////////////
    
    path('completar_mensajeIMP/<int:mensaje_id>/', views.completar_mensajeIMP, name='completar_mensajeIMP'),    
    path('generate_pdfIMP/<int:task_id>/', views.generate_pdfIMP, name='generate_pdfIMP'),


    # Inmuebles
    path('inmuebles/', views.inmuebles_list, name='inmuebles_list'),
    path("inmuebles/<int:pk>/", views.detalle_inmueble, name="detalle_inmueble"),
    path('inmuebles/crear/', views.crear_inmueble, name='crear_inmueble'),


    # Llamadas
    path("tareas/", views.tareas_list, name="tareas_list"),
    path("tareas/<int:pk>/", views.task_detail_llamadas, name="task_detail_llamadas"),
    path("tareas/<int:pk>/add-llamada/", views.registro_llamada, name="registro_llamada"),
    path("tareas/crear/", views.crear_tarea, name="crear_tarea"),
    path("tareas/buscar-inmuebles/", views.buscar_inmuebles_ajax, name="buscar_inmuebles_ajax"),
    path('tareas/exportar/', views.export_Llamadas_to_excelIMP, name='export_llamadas_excel'),
    path('export_tasks_to_excelIMP/', views.export_tasks_to_excelIMP, name='export_tasks_to_excelIMP'),


    path('importar/', views.importar, name='importar'),
    path('importar_Llamadas/', views.importar_Llamadas, name='importar_Llamadas'),
    path('contacto/', views.contacto, name='contacto'),

    
    # CONDIA ------------------------------------------------------------------
    # path('keep_session_alive/', views.keep_session_alive, name='keep_session_alive'),

    
    path('signupCondia/', views_condia.signupCondia, name='signupCondia'),
    path('signinCondia/', views_condia.signinCondia, name='signinCondia'),
    path('logout_condia/', views_condia.signout_condia, name='logout_condia'),
    path('task_condia/', views_condia.task_condia, name='task_condia'),
    path('create_task_CONDIA/', views_condia.create_task_CONDIA, name='create_task_CONDIA'),
    path('tasks/<int:task_id>/', views_condia.task_detail_condia, name='task_detail_condia'),



    # MDSJ SEP
    path('signout_MDSJ/', views_MDSJ.signout_MDSJ, name='signout_MDSJ'),
    path('signinMDSJ/', views_MDSJ.signinMDSJ, name='signinMDSJ'),
    path('signupMDSJ/', views_MDSJ.signupMDSJ, name='signupMDSJ'),
    path('task_salas/', views_MDSJ.task_salas, name='task_salas'),
    path('create_event/', views_MDSJ.create_event, name='create_event'),
    path('sala/<int:task_id>/', views_MDSJ.detail_event, name='detail_event'),

    path('salaJuntas/calendario/', views_MDSJ.calendar_MDSJ, name='calendar_MDSJ'),
    path('all_events_MDSJ/', views_MDSJ.all_events_MDSJ, name='all_events_MDSJ'), 
    path('add_event_MDSJ/', views_MDSJ.add_event_MDSJ, name='add_event_MDSJ'), 
    path('update_MDSJ/', views_MDSJ.update_MDSJ, name='update_MDSJ'),
    path('remove_MDSJ/', views_MDSJ.remove_MDSJ, name='remove_MDSJ'),
    path('salaJuntas/analicis/', views_MDSJ.uso_salas_view, name='uso_salas_view'),

]

handler404 = 'tasks.views.error_404'

from django.contrib.auth import logout  # Importa la función de logout

def custom_redirect(request, url):
    # Lista de URLs permitidas
    allowed_urls = ['signinMDSJ/', 'signupMDSJ/']

    # Verifica si la URL no se encuentra en la lista permitida
    if url not in allowed_urls:
        # Limpia la sesión antes de redirigir
        logout(request)
        # Redirige al inicio de sesión
        return redirect('signin')
    else:
        return None

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)