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
from django.urls import path
from djangocrud import settings
from tasks import views

urlpatterns = [
    path('', views.tasks, name='tasks'),
    path('tasks_importados/', views.tasks_importados, name='tasks_importados'),
    path('tasks/<int:task_id>', views.task_detail_importados, name='task_detail_importados'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks_completed_importados/', views.tasks_completed_importados, name='tasks_completed_importados'),
    path('inmuebles_baja/', views.inmuebles_baja, name='inmuebles_baja'),
    path('inmuebles_baja_importados/', views.inmuebles_baja_importados, name='inmuebles_baja_importados'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create_task/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/complete_importados', views.complete_task_importados, name='complete_task_importados'),
    path('tasks/<int:task_id>/bajas', views.bajas, name='bajas'),
    path('tasks/<int:task_id>/bajas_importados', views.bajas_importados, name='bajas_importados'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('principal/', views.principal, name='principal'),
    path('task/<int:task_id>/delete/', views.TaskDeleteView.as_view(), name='delete_task'),
    path('get_entidades_federativas/', views.get_entidades_federativas, name='get_entidades_federativas'),
    path('get_municipios/<str:entidad_federativa>/', views.get_municipios_by_entidad_federativa, name='get_municipios'),
    path('task/<int:task_id>/delete_expediente_cedoc/<int:expediente_cedoc_id>/', views.delete_expediente_cedoc, name='delete_expediente_cedoc'),
    path('task/<int:task_id>/delete_folio_real/<int:folio_real_id>/', views.delete_folio_real, name='delete_folio_real'),
    path('task/<int:task_id>/delete_numero_plano/<int:numero_plano_id>/', views.delete_numero_plano, name='delete_numero_plano'),
    path('editar_edificacion/<int:edificacion_id>/', views.editar_edificacion, name='editar_edificacion'),
    path('borrar_edificacion/<int:edificacion_id>/', views.borrar_edificacion, name='borrar_edificacion'),
    path('task/<int:task_id>/delete_edificio_verde/<int:edificio_verde_id>/', views.delete_edificio_verde, name='delete_edificio_verde'),

    
    # path('get_secciones_inventario/', views.get_secciones_inventario, name='get_secciones_inventario'),
    # path('get_dependencias_administradoras_by_seccion/<str:seccion_inventario>/', views.get_dependencias_administradoras_by_seccion, name='get_dependencias_administradoras_by_seccion'),
    # path('get_subsecciones_by_dependencia_administradora/<str:seccion_inventario>/<str:dependencia_administradora>/', views.get_subsecciones_by_dependencia_administradora, name='get_subsecciones_by_dependencia_administradora'),
    
    # ///////////////////////////////////////////////////////////////////////////////////////////////
    
    path('guardar_docPropiedad/<int:task_id>/', views.guardar_docPropiedad, name='guardar_docPropiedad'),
    path('editar_documento/<int:documento_id>/', views.editar_documento, name='editar_documento'),
    path('eliminar_documento/<int:documento_id>/', views.eliminar_documento, name='eliminar_documento'),
    
    path('editar_documentoIMP/<int:documento_id>/', views.editar_documentoIMP, name='editar_documentoIMP'),
    path('eliminar_documentoIMP/<int:documento_id>/', views.eliminar_documentoIMP, name='eliminar_documentoIMP'),
    
    path('guardar_docPropiedadIMP/<int:task_id>/', views.guardar_docPropiedadIMP, name='guardar_docPropiedadIMP'),
    
    path('guardar_Avaluo/<int:task_id>/', views.guardar_Avaluo, name='guardar_Avaluo'),
    path('editar_avaluo/<int:avaluo_id>/', views.editar_avaluo, name='editar_avaluo'),
    path('eliminar_avaluo/<int:avaluo_id>/', views.eliminar_avaluo, name='eliminar_avaluo'),
    
    path('guardar_AvaluoIMP/<int:task_id>/', views.guardar_AvaluoIMP, name='guardar_AvaluoIMP'),
    path('editar_avaluoIMP/<int:avaluo_id>/', views.editar_avaluoIMP, name='editar_avaluoIMP'),
    path('eliminar_avaluoIMP/<int:avaluo_id>/', views.eliminar_avaluoIMP, name='eliminar_avaluoIMP'),
    
    path('guardar_documento_ocupacion/<int:task_id>/', views.guardar_documento_ocupacion, name='guardar_documento_ocupacion'),
    path('eliminar_docOcupacion/<int:docOcupacion_id>/', views.eliminar_docOcupacion, name='eliminar_docOcupacion'),
    
    path('guardar_instituciones_ocupantes/<int:task_id>/', views.guardar_instituciones_ocupantes, name='guardar_instituciones_ocupantes'),
    path('eliminar_DatoInstitucionOcupante/<int:datoInstitucionOcupante_id>/', views.eliminar_DatoInstitucionOcupante, name='eliminar_DatoInstitucionOcupante'),
    
    path('guardar_datos_terceros/<int:task_id>/', views.guardar_datos_terceros, name='guardar_datos_terceros'),
    path('deleteDatosTerceros/<int:datos_terceros_id>/', views.deleteDatosTerceros, name='deleteDatosTerceros'),
    
    path('guardar_documento_ocupacionIMP/<int:task_id>/', views.guardar_documento_ocupacionIMP, name='guardar_documento_ocupacionIMP'),
    path('eliminar_docOcupacionIMP/<int:docOcupacion_id>/', views.eliminar_docOcupacionIMP, name='eliminar_docOcupacionIMP'),
    
    path('guardar_instituciones_ocupantesIMP/<int:task_id>/', views.guardar_instituciones_ocupantesIMP, name='guardar_instituciones_ocupantesIMP'),
    path('eliminar_DatoInstitucionOcupanteIMP/<int:datoInstitucionOcupante_id>/', views.eliminar_DatoInstitucionOcupanteIMP, name='eliminar_DatoInstitucionOcupanteIMP'),
    
    path('guardar_datos_tercerosIMP/<int:task_id>/', views.guardar_datos_tercerosIMP, name='guardar_datos_tercerosIMP'),
    path('deleteDatosTercerosIMP/<int:datos_terceros_id>/', views.deleteDatosTercerosIMP, name='deleteDatosTercerosIMP'),
     
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),

    path('guardar_Ocupaciones/<int:task_id>/', views.guardar_Ocupaciones, name='guardar_Ocupaciones'),
    path('editar_ocupacion/<int:ocupacion_id>/', views.editar_ocupacion, name='editar_ocupacion'),
    path('eliminar_ocupacion/<int:ocupacion_id>/', views.eliminar_ocupacion, name='eliminar_ocupacion'),
    
    path('guardar_OcupacionesIMP/<int:task_id>/', views.guardar_OcupacionesIMP, name='guardar_OcupacionesIMP'),
    path('editar_ocupacionIMP/<int:ocupacion_id>/', views.editar_ocupacionIMP, name='editar_ocupacionIMP'),
    path('eliminar_ocupacionIMP/<int:ocupacion_id>/', views.eliminar_ocupacionIMP, name='eliminar_ocupacionIMP'),
    
    path('generate_pdf/<int:task_id>/', views.generate_pdf, name='generate_pdf'),

    path('export_tasks_to_excel/', views.export_tasks_to_excel, name='export_tasks_to_excel'),
    path('task/<int:task_id>/delete_tramite/<int:tramite_id>/', views.delete_tramite, name='delete_tramite'),
    
    
    path('dar_de_baja_task/<int:task_id>/', views.dar_de_baja_task, name='dar_de_baja_task'),
    path('importar/', views.importar, name='importar'),


    path('task/<int:task_id>/delete_expediente_cedocIMP/<int:expediente_cedoc_id>/', views.delete_expediente_cedocIMP, name='delete_expediente_cedocIMP'),
    path('task/<int:task_id>/delete_folio_realIMP/<int:folio_real_id>/', views.delete_folio_realIMP, name='delete_folio_realIMP'),
    path('task/<int:task_id>/delete_numero_planoIMP/<int:numero_plano_id>/', views.delete_numero_planoIMP, name='delete_numero_planoIMP'),
    path('task/<int:task_id>/delete_edificio_verdeIMP/<int:edificio_verde_id>/', views.delete_edificio_verdeIMP, name='delete_edificio_verdeIMP'),
    
    path('editar_edificacionIMP/<int:edificacion_id>/', views.editar_edificacionIMP, name='editar_edificacionIMP'),
    path('borrar_edificacionIMP/<int:edificacion_id>/', views.borrar_edificacionIMP, name='borrar_edificacionIMP'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)