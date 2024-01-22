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
from django.urls import include, path
from djangocrud import settings
from tasks import views
from condia import views as views_condia

app_name = 'tasks'

urlpatterns = [
    path('', views.tasks_importados, name='tasks_importados'),
    # path('tasks_importados/', views.tasks_importados, name='tasks_importados'),
    path('tasks/<int:task_id>', views.task_detail_importados, name='task_detail_importados'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('tasks_completed_importados/', views.tasks_completed_importados, name='tasks_completed_importados'),
    path('inmuebles_baja_importados/', views.inmuebles_baja_importados, name='inmuebles_baja_importados'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create_task/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/complete_importados', views.complete_task_importados, name='complete_task_importados'),
    path('tasks/<int:task_id>/bajas_importados', views.bajas_importados, name='bajas_importados'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('principal/', views.principal, name='principal'),
    path('task/<int:task_id>/delete/', views.TaskDeleteView.as_view(), name='delete_task'),
    path('get_entidades_federativas/', views.get_entidades_federativas, name='get_entidades_federativas'),
    path('get_municipios/<str:entidad_federativa>/', views.get_municipios_by_entidad_federativa, name='get_municipios'),
    path('agregar_dictamen_estructural<int:task_id>/', views.agregar_dictamen_estructural, name='agregar_dictamen_estructural'),
    path('agregar_folio_real/<int:task_id>/', views.agregar_folio_real, name='agregar_folio_real'),
    path('agregar_no_plano/<int:task_id>/', views.agregar_no_plano, name='agregar_no_plano'),
    path('agregar_expediente_CEDOC/<int:task_id>/', views.agregar_expediente_CEDOC, name='agregar_expediente_CEDOC'),
    # path('get_secciones_inventario/', views.get_secciones_inventario, name='get_secciones_inventario'),
    # path('get_dependencias_administradoras_by_seccion/<str:seccion_inventario>/', views.get_dependencias_administradoras_by_seccion, name='get_dependencias_administradoras_by_seccion'),
    # path('get_subsecciones_by_dependencia_administradora/<str:seccion_inventario>/<str:dependencia_administradora>/', views.get_subsecciones_by_dependencia_administradora, name='get_subsecciones_by_dependencia_administradora'),
    
    # ///////////////////////////////////////////////////////////////////////////////////////////////
    
    path('completar_mensajeIMP/<int:mensaje_id>/', views.completar_mensajeIMP, name='completar_mensajeIMP'),
    
    path('editar_documentoIMP/<int:documento_id>/', views.editar_documentoIMP, name='editar_documentoIMP'),
    path('eliminar_documentoIMP/<int:documento_id>/', views.eliminar_documentoIMP, name='eliminar_documentoIMP'),
    
    path('guardar_docPropiedadIMP/<int:task_id>/', views.guardar_docPropiedadIMP, name='guardar_docPropiedadIMP'),
    
    
    path('guardar_AvaluoIMP/<int:task_id>/', views.guardar_AvaluoIMP, name='guardar_AvaluoIMP'),
    path('editar_avaluoIMP/<int:avaluo_id>/', views.editar_avaluoIMP, name='editar_avaluoIMP'),
    path('eliminar_avaluoIMP/<int:avaluo_id>/', views.eliminar_avaluoIMP, name='eliminar_avaluoIMP'),
    
    path('eliminar_dictamenIMP/<int:dictamen_estructural_id>/', views.eliminar_dictamenIMP, name='eliminar_dictamenIMP'),
    
    path('guardar_documento_ocupacionIMP/<int:task_id>/', views.guardar_documento_ocupacionIMP, name='guardar_documento_ocupacionIMP'),
    path('eliminar_docOcupacionIMP/<int:docOcupacion_id>/', views.eliminar_docOcupacionIMP, name='eliminar_docOcupacionIMP'),
    
    path('guardar_instituciones_ocupantesIMP/<int:task_id>/', views.guardar_instituciones_ocupantesIMP, name='guardar_instituciones_ocupantesIMP'),
    path('eliminar_DatoInstitucionOcupanteIMP/<int:datoInstitucionOcupante_id>/', views.eliminar_DatoInstitucionOcupanteIMP, name='eliminar_DatoInstitucionOcupanteIMP'),
    
    path('guardar_datos_tercerosIMP/<int:task_id>/', views.guardar_datos_tercerosIMP, name='guardar_datos_tercerosIMP'),
    path('deleteDatosTercerosIMP/<int:datos_terceros_id>/', views.deleteDatosTercerosIMP, name='deleteDatosTercerosIMP'),
     
    
    path('guardar_OcupacionesIMP/<int:task_id>/', views.guardar_OcupacionesIMP, name='guardar_OcupacionesIMP'),
    path('editar_ocupacionIMP/<int:ocupacion_id>/', views.editar_ocupacionIMP, name='editar_ocupacionIMP'),
    path('eliminar_ocupacionIMP/<int:ocupacion_id>/', views.eliminar_ocupacionIMP, name='eliminar_ocupacionIMP'),
    
    path('generate_pdfIMP/<int:task_id>/', views.generate_pdfIMP, name='generate_pdfIMP'),

    path('export_tasks_to_excelIMP/', views.export_tasks_to_excelIMP, name='export_tasks_to_excelIMP'),
    
    

    
    path('importar/', views.importar, name='importar'),


    path('task/<int:task_id>/delete_expediente_cedocIMP/<int:expediente_cedoc_id>/', views.delete_expediente_cedocIMP, name='delete_expediente_cedocIMP'),
    path('task/<int:task_id>/delete_folio_realIMP/<int:folio_real_id>/', views.delete_folio_realIMP, name='delete_folio_realIMP'),
    path('task/<int:task_id>/delete_numero_planoIMP/<int:numero_plano_id>/', views.delete_numero_planoIMP, name='delete_numero_planoIMP'),
    path('task/<int:task_id>/delete_edificio_verdeIMP/<int:edificio_verde_id>/', views.delete_edificio_verdeIMP, name='delete_edificio_verdeIMP'),
    
    path('editar_edificacionIMP/<int:edificacion_id>/', views.editar_edificacionIMP, name='editar_edificacionIMP'),
    path('borrar_edificacionIMP/<int:edificacion_id>/', views.borrar_edificacionIMP, name='borrar_edificacionIMP'),
    
    path('task/<int:task_id>/delete_ColindanciaIMP/<int:colindancia_id>/', views.delete_ColindanciaIMP, name='delete_ColindanciaIMP'),
    
    path('calendar/', views.calendar, name='calendar'),
    
    # CONDIA ------------------------------------------------------------------
    path('keep_session_alive/', views.keep_session_alive, name='keep_session_alive'),

    
    path('signupCondia/', views_condia.signupCondia, name='signupCondia'),
    path('signinCondia/', views_condia.signinCondia, name='signinCondia'),
    
    path('logout_condia/', views_condia.signout_condia, name='logout_condia'),
    
    path('task_condia/', views_condia.task_condia, name='task_condia'),
    
    path('create_task_CONDIA/', views_condia.create_task_CONDIA, name='create_task_CONDIA'),
    
    path('tasks/<int:task_id>/', views_condia.task_detail_condia, name='task_detail_condia'),
    path('all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove')
    

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)